from enum import StrEnum


class AssistanceSegment(StrEnum):
    children_in_hospital = "Детям в больницах"
    children_in_orphanages = "Детям в детских домах"
    disabled_children = "Семьям с детьми-инвалидами"
    auto_volunteer = "Могу автоволонтерить"
    not_decide = "Еще не определился"
