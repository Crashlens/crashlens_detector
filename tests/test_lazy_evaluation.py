"""
Tests for lazy evaluation optimization in Crashens Detector
"""

import pytest
from crashlens.detectors.retry_loops import RetryLoopDetector
from crashlens.detectors.fallback_storm import FallbackStormDetector
from crashlens.detectors.fallback_failure import FallbackFailureDetector
from crashlens.detectors.overkill_model_detector import OverkillModelDetector


class TestLazyEvaluation:
    """Test that detectors exit early once a trace is flagged"""

    def test_retry_loop_detector_lazy_evaluation(self):
        """Test that RetryLoopDetector exits early after flagging a trace"""
        detector = RetryLoopDetector(max_retries=2, time_window_minutes=5)
        
        # Create traces with retry loops
        traces = {
            "trace_1": [
                {"traceId": "trace_1", "model": "gpt-4", "prompt": "test", "startTime": "2025-01-01T10:00:00Z"},
                {"traceId": "trace_1", "model": "gpt-4", "prompt": "test", "startTime": "2025-01-01T10:00:01Z"},
                {"traceId": "trace_1", "model": "gpt-4", "prompt": "test", "startTime": "2025-01-01T10:00:02Z"},
            ],
            "trace_2": [
                {"traceId": "trace_2", "model": "gpt-4", "prompt": "test2", "startTime": "2025-01-01T10:00:00Z"},
                {"traceId": "trace_2", "model": "gpt-4", "prompt": "test2", "startTime": "2025-01-01T10:00:01Z"},
                {"traceId": "trace_2", "model": "gpt-4", "prompt": "test2", "startTime": "2025-01-01T10:00:02Z"},
            ]
        }
        
        detections = detector.detect(traces)
        
        # Should only detect one trace due to lazy evaluation
        assert len(detections) == 1
        assert detections[0]["trace_id"] == "trace_1"

    def test_fallback_storm_detector_lazy_evaluation(self):
        """Test that FallbackStormDetector exits early after flagging a trace"""
        detector = FallbackStormDetector(min_calls=3, min_models=2)
        
        # Create traces with fallback storms
        traces = {
            "trace_1": [
                {"traceId": "trace_1", "model": "gpt-3.5-turbo", "startTime": "2025-01-01T10:00:00Z"},
                {"traceId": "trace_1", "model": "gpt-4", "startTime": "2025-01-01T10:00:01Z"},
                {"traceId": "trace_1", "model": "claude-3-sonnet", "startTime": "2025-01-01T10:00:02Z"},
            ],
            "trace_2": [
                {"traceId": "trace_2", "model": "gpt-3.5-turbo", "startTime": "2025-01-01T10:00:00Z"},
                {"traceId": "trace_2", "model": "gpt-4", "startTime": "2025-01-01T10:00:01Z"},
                {"traceId": "trace_2", "model": "claude-3-sonnet", "startTime": "2025-01-01T10:00:02Z"},
            ]
        }
        
        detections = detector.detect(traces)
        
        # Should only detect one trace due to lazy evaluation
        assert len(detections) == 1
        assert detections[0]["trace_id"] == "trace_1"

    def test_fallback_failure_detector_lazy_evaluation(self):
        """Test that FallbackFailureDetector exits early after flagging a trace"""
        detector = FallbackFailureDetector()
        
        # Create traces with fallback failures - need proper format with usage data
        traces = {
            "trace_1": [
                {
                    "traceId": "trace_1", 
                    "model": "gpt-3.5-turbo", 
                    "startTime": "2025-01-01T10:00:00Z", 
                    "usage": {"completion_tokens": 10},  # Indicates success
                    "prompt": "What is 2+2?"
                },
                {
                    "traceId": "trace_1", 
                    "model": "gpt-4", 
                    "startTime": "2025-01-01T10:00:01Z", 
                    "usage": {"completion_tokens": 5},
                    "prompt": "What is 2+2?"  # Same prompt
                },
            ],
            "trace_2": [
                {
                    "traceId": "trace_2", 
                    "model": "gpt-3.5-turbo", 
                    "startTime": "2025-01-01T10:00:00Z", 
                    "usage": {"completion_tokens": 10},
                    "prompt": "What is 3+3?"
                },
                {
                    "traceId": "trace_2", 
                    "model": "gpt-4", 
                    "startTime": "2025-01-01T10:00:01Z", 
                    "usage": {"completion_tokens": 5},
                    "prompt": "What is 3+3?"  # Same prompt
                },
            ]
        }
        
        detections = detector.detect(traces)
        
        # Should only detect one trace due to lazy evaluation
        assert len(detections) == 1
        assert detections[0]["trace_id"] == "trace_1"

    def test_overkill_model_detector_lazy_evaluation(self):
        """Test that OverkillModelDetector exits early after flagging a trace"""
        detector = OverkillModelDetector(max_prompt_tokens=50, max_prompt_chars=200)
        
        # Create traces with overkill model usage
        traces = {
            "trace_1": [
                {"traceId": "trace_1", "model": "gpt-4", "prompt": "What is 2+2?", "startTime": "2025-01-01T10:00:00Z"},
            ],
            "trace_2": [
                {"traceId": "trace_2", "model": "gpt-4", "prompt": "What is 3+3?", "startTime": "2025-01-01T10:00:00Z"},
            ]
        }
        
        detections = detector.detect(traces)
        
        # Should only detect one trace due to lazy evaluation
        assert len(detections) == 1
        assert detections[0]["trace_id"] == "trace_1"

    def test_already_flagged_suppression(self):
        """Test that detectors properly skip already flagged traces"""
        detector = RetryLoopDetector(max_retries=2, time_window_minutes=5)
        
        traces = {
            "trace_1": [
                {"traceId": "trace_1", "model": "gpt-4", "prompt": "test", "startTime": "2025-01-01T10:00:00Z"},
                {"traceId": "trace_1", "model": "gpt-4", "prompt": "test", "startTime": "2025-01-01T10:00:01Z"},
                {"traceId": "trace_1", "model": "gpt-4", "prompt": "test", "startTime": "2025-01-01T10:00:02Z"},
            ],
            "trace_2": [
                {"traceId": "trace_2", "model": "gpt-4", "prompt": "test2", "startTime": "2025-01-01T10:00:00Z"},
                {"traceId": "trace_2", "model": "gpt-4", "prompt": "test2", "startTime": "2025-01-01T10:00:01Z"},
                {"traceId": "trace_2", "model": "gpt-4", "prompt": "test2", "startTime": "2025-01-01T10:00:02Z"},
            ]
        }
        
        # Test with already flagged trace
        already_flagged = {"trace_1"}
        detections = detector.detect(traces, already_flagged_ids=already_flagged)
        
        # Should detect trace_2 since trace_1 is already flagged
        assert len(detections) == 1
        assert detections[0]["trace_id"] == "trace_2"
