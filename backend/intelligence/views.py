
from django.conf import settings
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from groq import Groq

from .models import Analysis
from .serializers import AnalysisSerializer


class AnalysisViewSet(viewsets.ModelViewSet):
    serializer_class = AnalysisSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Analysis.objects.all().order_by("-created_at")

        return Analysis.objects.filter(
            created_by=self.request.user
        ).order_by("-created_at")


class AIChatView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        prompt = str(request.data.get("prompt", "")).strip()

        if not prompt:
            return Response(
                {"error": "Prompt is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        api_key = getattr(settings, "GROQ_API_KEY", "")

        if not api_key:
            return Response(
                {"error": "GROQ_API_KEY is not configured"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        save_analysis = request.data.get("save", True)

        try:
            client = Groq(api_key=api_key)

            completion = client.chat.completions.create(
                model=getattr(
                    settings,
                    "GROQ_MODEL",
                    "llama-3.3-70b-versatile",
                ),
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are FIDS AI, a professional football "
                            "intelligence assistant. Analyze football "
                            "matches, teams, players, tactics, and news. "
                            "Be clear, structured, and honest. Never "
                            "invent live statistics or match results."
                        ),
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                temperature=0.5,
                max_tokens=1500,
            )

            answer = completion.choices[0].message.content or ""

            analysis_id = None

            if save_analysis:
                analysis = Analysis.objects.create(
                    title=prompt[:200],
                    analysis_type=self.detect_analysis_type(prompt),
                    summary=answer,
                    data={
                        "prompt": prompt,
                        "provider": "groq",
                        "model": getattr(
                            settings,
                            "GROQ_MODEL",
                            "llama-3.3-70b-versatile",
                        ),
                    },
                    created_by=request.user,
                )
                analysis_id = analysis.id

            return Response({
                "success": True,
                "answer": answer,
                "saved": bool(save_analysis),
                "analysis_id": analysis_id,
                "provider": "groq",
            })

        except Exception as error:
            return Response(
                {
                    "success": False,
                    "error": str(error),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @staticmethod
    def detect_analysis_type(prompt):
        prompt = prompt.lower()

        if any(word in prompt for word in ["player", "ميسي", "صلاح"]):
            return Analysis.AnalysisType.PLAYER

        if any(word in prompt for word in ["team", "club", "فريق"]):
            return Analysis.AnalysisType.TEAM

        return Analysis.AnalysisType.MATCH
