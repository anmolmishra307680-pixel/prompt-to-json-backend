import json
from datetime import datetime
from pathlib import Path
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from schema import DesignSpec, EvaluationResult

class ReportGenerator:
    def __init__(self, reports_dir: str = "reports"):
        self.reports_dir = Path(reports_dir)
        self.reports_dir.mkdir(exist_ok=True)

    def generate_report(self, spec: DesignSpec, evaluation: EvaluationResult, prompt: str = "") -> str:
        """Generate evaluation report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.reports_dir / f"evaluation_report_{timestamp}.json"

        report_data = {
            "timestamp": datetime.now().isoformat(),
            "prompt": prompt,
            "design_specification": spec.model_dump(),
            "evaluation_results": evaluation.model_dump(),
            "summary": {
                "overall_score": evaluation.score,
                "grade": self._get_grade(evaluation.score),
                "key_issues": evaluation.feedback[:3],
                "top_suggestions": evaluation.suggestions[:3]
            }
        }

        with open(report_file, 'w') as f:
            json.dump(report_data, f, indent=2, default=str)

        return str(report_file)

    def _get_grade(self, score: float) -> str:
        """Convert score to letter grade"""
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        else:
            return "F"

    def generate_summary_report(self, reports_data: list) -> str:
        """Generate summary report from multiple evaluations"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        summary_file = self.reports_dir / f"summary_report_{timestamp}.json"

        if not reports_data:
            return str(summary_file)

        scores = [r["evaluation_results"]["score"] for r in reports_data]

        summary = {
            "timestamp": datetime.now().isoformat(),
            "total_evaluations": len(reports_data),
            "average_score": sum(scores) / len(scores),
            "highest_score": max(scores),
            "lowest_score": min(scores),
            "grade_distribution": self._calculate_grade_distribution(scores),
            "common_issues": self._find_common_issues(reports_data)
        }

        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)

        return str(summary_file)

    def _calculate_grade_distribution(self, scores: list) -> dict:
        """Calculate distribution of grades"""
        grades = [self._get_grade(score) for score in scores]
        distribution = {}
        for grade in ['A', 'B', 'C', 'D', 'F']:
            distribution[grade] = grades.count(grade)
        return distribution

    def _find_common_issues(self, reports_data: list) -> list:
        """Find most common issues across reports"""
        all_feedback = []
        for report in reports_data:
            all_feedback.extend(report["evaluation_results"]["feedback"])

        # Simple frequency count
        issue_counts = {}
        for feedback in all_feedback:
            issue_counts[feedback] = issue_counts.get(feedback, 0) + 1

        # Return top 5 most common issues
        return sorted(issue_counts.items(), key=lambda x: x[1], reverse=True)[:5]
