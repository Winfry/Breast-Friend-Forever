import 'package:flutter/foundation.dart';
import 'package:shared_preferences/shared_preferences.dart';

class ProgressProvider with ChangeNotifier {
  List<int> _completedExamSteps = [];

  List<int> get completedExamSteps => _completedExamSteps;

  ProgressProvider() {
    _loadProgress();
  }

  Future<void> _loadProgress() async {
    final prefs = await SharedPreferences.getInstance();
    final steps = prefs.getStringList('completed_exam_steps');
    if (steps != null) {
      _completedExamSteps = steps.map(int.parse).toList();
      notifyListeners();
    }
  }

  Future<void> completeExamStep(int stepId) async {
    if (!_completedExamSteps.contains(stepId)) {
      _completedExamSteps.add(stepId);
      await _saveProgress();
      notifyListeners();
    }
  }

  Future<void> _saveProgress() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setStringList(
      'completed_exam_steps',
      _completedExamSteps.map((e) => e.toString()).toList(),
    );
  }

  void resetProgress() {
    _completedExamSteps.clear();
    _saveProgress();
    notifyListeners();
  }
}