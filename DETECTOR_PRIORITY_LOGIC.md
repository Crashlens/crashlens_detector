# 🔍 Crashlens Detector Priority Logic - Detailed Technical Explanation

## Overview

The Crashlens Detector uses a sophisticated **priority-based suppression system** to prevent double-counting waste patterns and ensure accurate root cause attribution. This system ensures that when multiple waste patterns occur in the same trace, only the most fundamental issue is reported.

## 🎯 Core Priority Ranking

The detectors are ordered by priority (1 = highest priority, 4 = lowest):

```python
DETECTOR_PRIORITY = {
    "RetryLoopDetector": 1,      # Highest priority - fundamental infrastructure issue
    "FallbackStormDetector": 2,  # Model switching chaos
    "FallbackFailureDetector": 3, # Unnecessary expensive calls
    "OverkillModelDetector": 4,   # Overkill for simple tasks - lowest priority
}
```

## 🧠 Priority Rationale

### 1. **RetryLoopDetector** (Priority 1 - Highest)
- **Why highest:** Represents a **fundamental infrastructure or logic problem**
- **Root cause:** Usually indicates broken error handling, network issues, or faulty retry logic
- **Impact:** If you fix the retry loop, the other issues might disappear entirely
- **Example:** If your code retries the same GPT-4 call 10 times due to a bug, the "overkill model usage" is secondary to fixing the retry bug

### 2. **FallbackStormDetector** (Priority 2)
- **Why second:** Indicates **chaotic model selection logic** that needs systematic fixes
- **Root cause:** Poor model routing, cascading failures, or missing circuit breakers
- **Impact:** Fixing model selection logic addresses multiple efficiency issues
- **Example:** If your code tries GPT-3.5 → GPT-4 → Claude → GPT-4 for the same task, that's more important than just flagging the individual expensive calls

### 3. **FallbackFailureDetector** (Priority 3)
- **Why third:** Identifies **unnecessary redundant calls** but not systemic issues
- **Root cause:** Inefficient fallback logic or duplicate processing
- **Impact:** Specific optimization opportunity, but less fundamental than systemic issues
- **Example:** GPT-3.5 succeeds, but then GPT-4 is called anyway

### 4. **OverkillModelDetector** (Priority 4 - Lowest)
- **Why lowest:** Identifies **suboptimal model choice** but not broken logic
- **Root cause:** Model selection could be optimized, but the system is working correctly
- **Impact:** Cost optimization opportunity, but doesn't indicate broken infrastructure
- **Example:** Using GPT-4 for "What is 2+2?" when GPT-3.5 would suffice

## 🔧 Technical Implementation

### Suppression Engine Architecture

The `SuppressionEngine` class implements trace-level ownership to prevent double-counting:

```python
class SuppressionEngine:
    def __init__(self):
        # Track which detector "owns" each trace
        self.trace_ownership: Dict[str, str] = {}  # {trace_id: detector_name}
        self.suppressed_detections: List[Dict] = []
        self.active_detections: List[Dict] = []
```

### Processing Flow

1. **Sequential Processing:** Detectors run in priority order (1, 2, 3, 4)
2. **Ownership Claiming:** First detector to flag a trace "claims" it
3. **Priority Checking:** Later detectors check if they have higher priority
4. **Ownership Transfer:** Higher priority detectors can "steal" ownership
5. **Suppression:** Lower priority detections are moved to suppressed list

### Detailed Algorithm

```python
def process_detections(self, detector_name: str, detections: List[Dict]) -> List[Dict]:
    """Process detections with priority-based suppression"""
    active = []
    
    for detection in detections:
        trace_id = detection.get("trace_id")
        
        # Check if trace already has an owner
        if trace_id in self.trace_ownership:
            current_owner = self.trace_ownership[trace_id]
            current_priority = DETECTOR_PRIORITY.get(detector_name, 999)
            owner_priority = DETECTOR_PRIORITY.get(current_owner, 999)
            
            # Lower number = higher priority
            if current_priority > owner_priority:
                # Current detector has LOWER priority, suppress this detection
                self._add_suppressed_detection(detection, detector_name, 
                    f"higher_priority_detector:{current_owner}")
                continue
            elif current_priority < owner_priority:
                # Current detector has HIGHER priority, transfer ownership
                self._transfer_ownership(trace_id, current_owner, detector_name)
        
        # This detection becomes active - claim ownership
        self.trace_ownership[trace_id] = detector_name
        active.append(detection)
    
    return active
```

## 📋 Configuration-Based Suppression Rules

In addition to priority-based suppression, the system supports configuration-based rules from `crashlens-policy.yaml`:

```yaml
suppression_rules:
  retry_loop:
    suppress_if_retry_loop: false  # Can't suppress itself
  
  fallback_storm:
    suppress_if_retry_loop: true   # Always suppressed by retry loops
  
  fallback_failure:
    suppress_if_retry_loop: true   # Always suppressed by retry loops
  
  overkill_model:
    suppress_if_retry_loop: false  # Independent analysis (not suppressed)
```

### Configuration Logic

```python
def _should_suppress_by_priority(self, detector_name: str, current_priority: int, owner_priority: int) -> bool:
    """Check if detector should be suppressed based on configuration"""
    detector_config = self.suppression_config.get(detector_name, {})
    
    # If suppress_if_retry_loop is False, allow coexistence
    if not detector_config.get("suppress_if_retry_loop", True):
        return False
    
    # Otherwise, use strict priority suppression
    return current_priority > owner_priority
```

## 🎯 Real-World Examples

### Example 1: Retry Loop Dominates Everything

**Scenario:** A trace has both retry loops AND expensive model usage

```json
// Trace: user_auth_001 - Same call repeated 5 times
{"traceId": "user_auth_001", "model": "gpt-4", "prompt": "Validate token", "startTime": "10:00:00Z"}
{"traceId": "user_auth_001", "model": "gpt-4", "prompt": "Validate token", "startTime": "10:00:01Z"}
{"traceId": "user_auth_001", "model": "gpt-4", "prompt": "Validate token", "startTime": "10:00:02Z"}
{"traceId": "user_auth_001", "model": "gpt-4", "prompt": "Validate token", "startTime": "10:00:03Z"}
{"traceId": "user_auth_001", "model": "gpt-4", "prompt": "Validate token", "startTime": "10:00:04Z"}
```

**Processing:**
1. **RetryLoopDetector** (Priority 1) runs first → Detects retry pattern → Claims trace `user_auth_001`
2. **OverkillModelDetector** (Priority 4) runs later → Sees expensive model for simple task → Checks ownership → Finds RetryLoopDetector owns it → **Suppresses its detection**

**Result:** Only retry loop is reported because fixing the retry bug is the root cause

### Example 2: Fallback Storm vs Individual Failures

**Scenario:** A trace switches between multiple models chaotically

```json
// Trace: content_gen_001 - Model switching chaos
{"traceId": "content_gen_001", "model": "gpt-3.5-turbo", "prompt": "Write blog post", "startTime": "10:00:00Z"}
{"traceId": "content_gen_001", "model": "gpt-4", "prompt": "Write blog post", "startTime": "10:00:05Z"}
{"traceId": "content_gen_001", "model": "claude-3-sonnet", "prompt": "Write blog post", "startTime": "10:00:10Z"}
{"traceId": "content_gen_001", "model": "gpt-4", "prompt": "Write blog post", "startTime": "10:00:15Z"}
```

**Processing:**
1. **RetryLoopDetector** (Priority 1) → No retry pattern detected
2. **FallbackStormDetector** (Priority 2) → Detects chaotic model switching → Claims trace
3. **FallbackFailureDetector** (Priority 3) → Would detect gpt-3.5 → gpt-4 fallback → Checks ownership → FallbackStormDetector owns it → **Suppresses its detection**

**Result:** Only fallback storm reported because the systemic model selection issue is more important than individual fallback instances

### Example 3: Independent Analysis (Overkill Model)

**Scenario:** Simple task with expensive model, but no retry loops

```json
// Trace: simple_math_001 - Just expensive model for simple task
{"traceId": "simple_math_001", "model": "gpt-4", "prompt": "What is 2+2?", "startTime": "10:00:00Z"}
```

**Processing:**
1. **RetryLoopDetector** (Priority 1) → No retry pattern
2. **FallbackStormDetector** (Priority 2) → No model switching
3. **FallbackFailureDetector** (Priority 3) → No fallback pattern
4. **OverkillModelDetector** (Priority 4) → Detects expensive model for simple task → Claims trace

**Result:** Overkill model detection is reported because no higher-priority issues exist

## 🔄 Ownership Transfer Logic

When a higher-priority detector encounters a trace already claimed by a lower-priority detector:

```python
def _transfer_ownership(self, trace_id: str, old_owner: str, new_owner: str):
    """Transfer ownership and move old detections to suppressed"""
    # Find active detections from old owner for this trace
    to_suppress = []
    remaining_active = []
    
    for detection in self.active_detections:
        if detection.get("trace_id") == trace_id and old_owner.lower() in detection.get("type", "").lower():
            to_suppress.append(detection)
        else:
            remaining_active.append(detection)
    
    # Move old detections to suppressed with reason
    for detection in to_suppress:
        self._add_suppressed_detection(detection, old_owner, f"superseded_by:{new_owner}")
    
    self.active_detections = remaining_active
    self.trace_ownership[trace_id] = new_owner
```

## 📊 Transparency and Debugging

The system provides full transparency into suppression decisions:

```python
def get_suppression_summary(self) -> Dict[str, Any]:
    """Generate detailed suppression summary"""
    return {
        "total_traces_analyzed": len(set(trace_ids)),
        "active_issues": len(self.active_detections),
        "suppressed_issues": len(self.suppressed_detections),
        "suppression_breakdown": {
            "higher_priority_detector": count,
            "disabled_by_config": count,
            "superseded_by": count
        },
        "trace_ownership": self.trace_ownership  # Which detector owns each trace
    }
```

## 🎯 Benefits of This System

1. **Prevents Double-Counting:** Same waste isn't reported by multiple detectors
2. **Root Cause Focus:** Prioritizes fundamental issues over symptoms
3. **Accurate Cost Attribution:** Waste totals are precise, not inflated
4. **Actionable Results:** Developers get clear guidance on what to fix first
5. **Configurable:** Rules can be adjusted based on organizational priorities
6. **Transparent:** Full visibility into what was suppressed and why

## 📈 Performance Considerations

- **Memory Efficient:** Only stores trace ownership mapping, not full detection data
- **O(n) Complexity:** Linear processing with minimal overhead
- **Lazy Evaluation:** Suppression decisions made during detection, not post-processing
- **Configurable Depth:** Can disable suppression for specific detector combinations

This priority system ensures that Crashlens Detector provides accurate, actionable insights that help developers fix the most important issues first, leading to maximum cost savings with minimal effort.
