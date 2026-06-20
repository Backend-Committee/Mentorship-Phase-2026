from rest_framework.routers import DefaultRouter
from workouts.views import WorkoutViewSet
from nutrition_tracker.views import NutritionLogViewSet

router = DefaultRouter()
router.register(r'workouts', WorkoutViewSet, basename='api-workout')
router.register(r'nutrition', NutritionLogViewSet, basename='api-nutrition')

urlpatterns = router.urls