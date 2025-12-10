from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class SymptomInput(BaseModel):
    symptoms: List[str]
    location: Optional[str] = None
    pain_level: int  # 0-10
    duration_days: int
    cycle_day: int  # Day of menstrual cycle (1-28+)
    is_breastfeeding: bool = False
    age: int

class AnalysisResult(BaseModel):
    risk_level: str  # "Low", "Moderate", "High"
    summary: str
    recommendation: str
    potential_causes: List[str]
    urgency: str  # "Routine", "Soon", "Immediate"

class SymptomExpertSystem:
    """
    A rule-based expert system for breast health symptom analysis.
    NOT a diagnostic tool. Provides educational guidance based on medical guidelines.
    """
    
    def analyze(self, data: SymptomInput) -> AnalysisResult:
        risk_score = 0
        potential_causes = []
        
        # --- 1. Symptom Analysis ---
        symptoms_lower = [s.lower() for s in data.symptoms]
        
        if data.location:
            potential_causes.append(f"Symptom located at: {data.location}")

        # High Risk Flags
        if "hard lump" in symptoms_lower or "fixed lump" in symptoms_lower:
            risk_score += 5
            potential_causes.append("Suspicious mass")
        
        if "nipple retraction" in symptoms_lower or "inverted nipple" in symptoms_lower:
            risk_score += 4
            potential_causes.append("Structural tissue change")
            
        if "bloody discharge" in symptoms_lower:
            risk_score += 5
            potential_causes.append("Ductal issue")
            
        if "skin dimpling" in symptoms_lower or "orange peel skin" in symptoms_lower:
            risk_score += 4
            potential_causes.append("Skin tethering")

        # Moderate Risk Flags
        if "soft lump" in symptoms_lower or "movable lump" in symptoms_lower:
            risk_score += 2
            potential_causes.append("Cyst or Fibroadenoma")
            
        if "pain" in symptoms_lower:
            # Pain is often hormonal, less likely cancer alone
            risk_score += 1
            potential_causes.append("Cyclical mastalgia")

        # --- 2. Contextual Factors ---
        
        # Cycle Context
        # Symptoms appearing just before period (Day 20-28) are often hormonal
        if 20 <= data.cycle_day <= 28 and "pain" in symptoms_lower:
            risk_score -= 1  # Reduce risk as it's likely hormonal
            potential_causes.append("PMS-related changes")
            
        # Duration
        if data.duration_days > 14: # Persisting through a full cycle
            risk_score += 2
        
        # Age Factor
        if data.age > 50:
            risk_score += 2
        elif data.age < 30:
            risk_score -= 1 # Statistically lower risk

        # --- 3. Decision Logic ---
        
        if risk_score >= 5:
            return AnalysisResult(
                risk_level="High",
                summary="Your symptoms show some signs that require medical attention.",
                recommendation="Please see a doctor for a clinical breast exam and possible imaging.",
                potential_causes=list(dict.fromkeys(potential_causes)),
                urgency="Immediate (Within 1-2 weeks)"
            )
        elif risk_score >= 3:
            return AnalysisResult(
                risk_level="Moderate",
                summary="These symptoms are likely benign but should be checked.",
                recommendation="Monitor for one full menstrual cycle. If it persists, see a doctor.",
                potential_causes=list(dict.fromkeys(potential_causes)),
                urgency="Soon (Within a month)"
            )
        else:
            return AnalysisResult(
                risk_level="Low",
                summary="Your symptoms appear consistent with normal hormonal changes or benign conditions.",
                recommendation="Continue monthly self-exams. Note if anything changes.",
                potential_causes=list(dict.fromkeys(potential_causes)) if potential_causes else ["Normal breast tissue"],
                urgency="Routine"
            )

# Singleton instance
expert_system = SymptomExpertSystem()
