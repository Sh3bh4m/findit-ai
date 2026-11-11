"""Run two safe reference paths without external dependencies."""

from findit_showcase import CurrentRecord, IndexedRecord, SemanticIndex, TaskStore, route_question
from findit_showcase.semantic import content_sha256


def main() -> None:
    store = TaskStore.synthetic()
    exact = "How many open tasks are assigned to me?"
    print(f"{exact} -> {route_question(exact).route.value} -> {store.count_tasks('user-001', 'open')}")

    record = CurrentRecord("note-01", "notes", "user-001", "Approval delayed awaiting review")
    index = SemanticIndex([
        IndexedRecord(record.record_id, record.collection, record.owner_id,
                      content_sha256(record.text), (0.9, 0.1))
    ])
    related = "Find discussions about approvals"
    hits = index.search((1.0, 0.0), authenticated_owner="user-001",
                        allowed_collection="notes", current_records={record.record_id: record})
    print(f"{related} -> {route_question(related).route.value} -> {len(hits)} verified hit(s)")


if __name__ == "__main__":
    main()
