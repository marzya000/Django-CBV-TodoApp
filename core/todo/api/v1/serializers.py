
from rest_framework import serializers # type: ignore
from todo.models import Task


class TaskSerializer(serializers.ModelSerializer):
    relative_url = serializers.URLField(source="get_absolute_api_url", read_only=True)
    absolute_url = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ["id", "title", "complete", "relative_url", "absolute_url"]
        read_only_fields = ["user"]


    def get_absolute_url(self, obj):
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(obj.get_absolute_api_url())
        return None

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        request = self.context.get("request")
        if request:
            kwargs = request.parser_context.get("kwargs", {})
            if "pk" in kwargs:
                rep.pop("relative_url", None)
                rep.pop("absolute_url", None)
        return rep
