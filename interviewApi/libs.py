from .models import Evaluation


def get_all_evaluation():
    return Evaluation.objects.all()




