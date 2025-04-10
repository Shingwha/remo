from typing import List, Dict, Optional, Literal, Union
from datetime import datetime
import json
import uuid


class Memory:
    def __init__(
        self,
        summary: str,
        keywords: List[str] = None,
        time: Optional[Dict[str, str]] = None,
        conversation: Optional[str] = None,
        type: Literal["USER", "SYSTEM", "TODO"] = "TODO",
        status: Optional[Literal["待更新"]] = "待更新",
        **kwargs,
    ):
        self.type = type
        self.summary = summary
        self.keywords = keywords
        self.time = time
        self.conversation = conversation
        self.id = self._generate_id()
        self.status = status

    def _generate_id(self):
        timestamp = datetime.now().strftime("%Y%m%d%H%M")
        unique_suffix = uuid.uuid4().hex[:2]  # 取UUID的hex表示的前2位
        return f"{self.type}_{timestamp}_{unique_suffix}"
    
    def update_memory(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
                

    def to_dict(self):
        return {
            "type": self.type,
            "summary": self.summary,
            "keywords": self.keywords,
            "time": self.time,
            "conversation": self.conversation,
            "id": self.id,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(
            type=data["type"],
            summary=data["summary"],
            keywords=data["keywords"],
            time=data["time"],
            conversation=data["conversation"],
            id=data["id"],
            status=data["status"],
        )


class MemoryBank:
    def __init__(self, storage_path: str = None):
        self.memories = {}
        self.storage_path = storage_path
        self._load_memories()

    def __iter__(self):
        return iter(self.memories.values())

    def _load_memories(self):
        if self.storage_path:
            try:
                with open(self.storage_path, "r", encoding='utf-8') as f:
                    content = f.read()
                    if content.strip():
                        data = json.loads(content)
                        for mem_data in data.values():
                            memory = Memory.from_dict(mem_data)
                            self.memories[memory.id] = memory
            except (FileNotFoundError, json.JSONDecodeError):
                pass

    def _save_to_storage(self) -> None:
        if self.storage_path:
            with open(self.storage_path, "w",encoding='utf-8') as f:
                json.dump(
                    {mid: m.to_dict() for mid, m in self.memories.items()}, f, indent=2
                )

    def add_memory_by_args(self, **kwargs) -> str:
        memory = Memory(**kwargs)
        self.memories[memory.id] = memory
        self._save_to_storage()
        return f"添加记忆成功，具体参数如下：{memory.to_dict()}"
    
    def add_memory(self,memory ) -> str:
        self.memories[memory.id] = memory
        self._save_to_storage()
        return f"添加记忆成功，具体参数如下：{memory.to_dict()}"
    
    def delete_memory_by_id(self, id: str) -> bool:
        """删除记忆"""
        if id in self.memories:
            memory_dict = self.memories[id].to_dict()
            self.memories.pop(id)
            self._save_to_storage()
            return f"删除记忆成功，具体参数如下：{memory_dict}"
        return f"删除记忆失败，ID<{id}>不存在"
    
    def update_memory_by_id(self, **kwargs) -> Optional[Memory]:
        """更新记忆"""
        id = kwargs.pop("id")
        if id not in self.memories:
            return None
        memory = self.memories[id]
        memory.update_memory(**kwargs)
        self._save_to_storage()
        return f"更新记忆成功，具体参数如下：{memory.to_dict()}"
            

    def search_memory_by_id(self, id: Union[str, Dict]) -> Optional[Memory]:
        """根据ID获取记忆"""
        memory = self.memories.get(id)
        if memory:
            return f"查询记忆成功，具体参数如下：{memory.to_dict()}"
        return f"查询记忆失败，ID<{id}>不存在"
    
    def to_dict(self):
        return {mid: m.to_dict() for mid, m in self.memories.items()}
    


def execute_memory_actions(memory_bank: MemoryBank, actions: List[Dict]):
    results = []
    available_actions = {
        "add_memory_by_args": memory_bank.add_memory_by_args,
        "delete_memory_by_id": memory_bank.delete_memory_by_id,
        "search_memory_by_id": memory_bank.search_memory_by_id,
        "update_memory_by_id": memory_bank.update_memory_by_id,
    }
    for action in actions:
        action_name = action["action"]
        action_args = action["args"]

        if action_name in available_actions:
            result = available_actions[action_name](**action_args)
            results.append(
                {"action": action_name, "args": action_args, "result": result}
            )
        else:
            results.append(
                {
                    "action": action_name,
                    "args": action_args,
                    "result": f"操作<{action_name}>不存在",
                }
            )

    return results
