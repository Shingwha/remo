from typing import List,Dict, Optional,Literal
from datetime import datetime
import json
import uuid

class Memory:
    
    def __init__(self,
        summary: str,
        keywords: List[str] = None,
        time: Optional[Dict[str, str]] = None,
        conversation: Optional[str] = None,
        type: Literal["LTM","TASK","TODO"] = "LTM",
        **kwargs):
        self.type = type
        self.summary = summary
        self.keywords = keywords
        self.time = time
        self.conversation = conversation
        self.id = self._generate_id()

    def _generate_id(self):
        timestamp = datetime.now().strftime("%Y%m%d%H%M")
        unique_suffix = uuid.uuid4().hex[:2]  # 取UUID的hex表示的前2位
        return f"{self.type}_{timestamp}_{unique_suffix}"

    def to_dict(self):
        return {
            "type": self.type,
            "summary": self.summary,
            "keywords": self.keywords,
            "time": self.time,
            "conversation": self.conversation,
            "id": self.id
        }

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(
            type=data["type"],
            summary=data["summary"],
            keywords=data["keywords"],
            time=data["time"],
            conversation=data["conversation"],
            id=data["id"]
        )




class MemoryBank:
    def __init__(self, storage_path: str=None):
        self.memories = {}
        self.storage_path = storage_path
        self._load_memories()

    def __iter__(self):
        return iter(self.memories.values())

    def _load_memories(self):
        if self.storage_path:
            try:
                with open(self.storage_path, "r") as f:
                    data = json.load(f)
                    for mem_data in data.values():
                        memory = Memory.from_dict(mem_data)
                        self.memories[memory.id] = memory
            except FileNotFoundError:
                pass

    def _save_to_storage(self) -> None:
        """保存记忆到文件"""
        if self.storage_path:
            with open(self.storage_path, "w") as f:
                json.dump(
                    {mid: m.to_dict() for mid, m in self.memories.items()}, 
                    f, 
                    indent=2
                )

    def add_memory(self, memory: Memory) -> str:
        """添加新记忆并返回ID"""
        self.memories[memory.id] = memory
        self._save_to_storage()
        return memory.id
    
    def forget(self, memory_id: str) -> bool:
        """删除记忆"""
        if memory_id in self.memories:
            del self.memories[memory_id]
            self._save_to_storage()
            return True
        return False

    def get_memory(self, memory_id: str) -> Optional[Memory]:
        """根据ID获取记忆"""
        return self.memories.get(memory_id)
    
    def search_memory(self, query: str) -> List[Memory]:
        pass
