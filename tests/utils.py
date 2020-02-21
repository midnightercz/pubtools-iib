from iiblib.iibclient import IIBBuildDetailsModel


class FakeTaskManager(object):
    def __init__(self):
        self.tasks = {}
        self.task_id = 0
        self.task_state_seq = {}

    def _gen_task_id(self):
        ret = "task-%d" % self.task_id
        self.task_id += 1
        return ret

    def setup_task(
        self,
        index,
        binary,
        bundles_map,
        arches,
        state_seq=("in_progress", "finished"),
        op_type="add",
    ):
        tid = self._gen_task_id()
        self.task_state_seq[tid] = list(state_seq)
        self.tasks[tid] = {
            "id": tid,
            "state": self.task_state_seq[tid].pop(0),
            "state_reason": "state_reason",
            "state_history": [],
            "from_index": index,
            "from_index_resolved": index + "-resolved",
            "operators": ["operator-%s" % k for k in bundles_map],
            "binary_image": binary,
            "binary_image_resolved": binary + "-resolved",
            "index_image": "index_image",
            "request_type": "request_type",
            "arches": arches,
        }

        if op_type == "add":
            self.tasks[tid]["bundles"] = bundles_map

        return self.tasks[tid]

    def get_task(self, tid):
        task = self.tasks[tid]
        state = self.task_state_seq[tid].pop(0)
        task["state"] = state
        return task


class FakeCollector(object):
    """Fake backend for PushCollector.
    Tests can access the attributes on this collector to see
    which push items & files were created during a task.
    """

    def __init__(self):
        self.items = []
        self.file_content = {}

    def update_push_items(self, items):
        self.items.extend(items)

    def attach_file(self, filename, content):
        self.file_content[filename] = content

    def append_file(self, filename, content):
        self.file_content[filename] = self.file_content.get(filename, b"") + content