"""Dependency-free, configuration-driven review-seat selection."""

from .rules import evaluate_panel, evaluate_record, evaluate_seat_wait, resolve

__all__ = ["evaluate_panel", "evaluate_record", "evaluate_seat_wait", "resolve"]
