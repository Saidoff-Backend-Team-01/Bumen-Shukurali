from subject.serializers import *
from subject.models import *
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.request import Request
# Create your views here.


class ClubList(ListAPIView):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer


class ClubDetail(RetrieveAPIView):
    queryset = Club.objects.all()
    serializer_class = ClubDatailSerializer


class SubjectList(ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class SubjectDetail(RetrieveAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

    def get(self, request, *args, **kwargs):
        subject = self.get_object()
        steps = Step.objects.filter(subject=subject)

        return Response({
            'data': SubjectSerializer(subject).data,
            'steps': StepSerializer(steps, many=True).data,
        })
    

class StepDetail(APIView):
    def get(self, req: Request, subject, step):
        try:
            subject = Subject.objects.get(pk=subject)
            step = Step.objects.filter(subject=subject).get(order=step)
            lessons = StepLesson.objects.filter(step=step)

            return Response({'step': StepSerializer(step).data, 'lessons': StepLessonSerializer(lessons, many=True).data})
        
        except:
            return Response({'error': 'Subject or step is wrong'}, status=404)
        

class LessonDetail(APIView):
    def get(self, req: Request, subject, step, lesson):
        try:
            subject = Subject.objects.get(pk=subject)
            step = Step.objects.filter(subject=subject).get(order=step)
            lesson_data = StepLesson.objects.filter(step=step).get(pk=lesson)

            return Response(StepLessonSerializer(lesson_data).data)
        
        except:
            return Response({'error': 'Something is wrong'}, status=404)