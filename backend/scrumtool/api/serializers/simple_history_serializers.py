from rest_framework import serializers
from simple_history.manager import HistoryManager


class HistoricalRecordField(serializers.ListField):
    child = serializers.DictField()

    def __init__(self, *args, **kwargs):
        self.histories = []
        super(HistoricalRecordField, self).__init__(*args, **kwargs)

    def to_representation(self, data: HistoryManager):
        print("---------------- called to repr -------------------")
        print(data)
        all_records = data.all()
        old_record = all_records.first()
        changes = {"field": None, "new": None, "old": None, }
        change_obj = {"user": None, "changes": []}
        for record in all_records:
            if record in self.histories:
                continue
            self.histories.append(record)
            delta = record.diff_against(old_record)
            old_record = record
            change_obj["user"] = record.history_user_id
            for change in delta.changes:
                changes["field"] = change.field
                changes["old"] = change.old
                changes["new"] = change.new
                change_obj["changes"].append(changes.copy())
                changes.clear()
            print("---------------- new change_obj -------------------")
            print(change_obj)
            break
        print("---------------- return to repr -------------------")
        return change_obj
