from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

# 关联的网站地址与核心关键词（作为示例数据）
REFERENCE_URL = "https://page-main-leyu.com.cn"
CORE_KEYWORD = "乐鱼体育"


@dataclass
class KeywordNote:
    """单个关键词笔记的数据结构"""
    keyword: str
    context: str
    source_url: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)

    def format_brief(self) -> str:
        """返回简短的单行描述"""
        tag_part = ", ".join(self.tags) if self.tags else "无标签"
        return f"[{self.keyword}] {self.context[:40]}... 标签: {tag_part}"

    def format_full(self) -> str:
        """返回包含元数据的完整文本"""
        lines = [
            f"关键词: {self.keyword}",
            f"描述: {self.context}",
            f"来源: {self.source_url or '未记录'}",
            f"标签: {', '.join(self.tags) if self.tags else '无'}",
            f"创建时间: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}",
        ]
        return "\n".join(lines)


@dataclass
class KeywordNotesCollection:
    """管理一组关键词笔记的集合"""
    notes: List[KeywordNote] = field(default_factory=list)
    name: str = "默认笔记集"

    def add_note(self, note: KeywordNote) -> None:
        """添加一条笔记到集合"""
        self.notes.append(note)

    def find_by_keyword(self, keyword: str) -> List[KeywordNote]:
        """按关键词精确查找"""
        return [n for n in self.notes if n.keyword == keyword]

    def find_by_tag(self, tag: str) -> List[KeywordNote]:
        """按标签查找"""
        return [n for n in self.notes if tag in n.tags]

    def format_all_brief(self) -> str:
        """将所有笔记用简短格式输出"""
        parts = [f"=== {self.name} ==="]
        for i, note in enumerate(self.notes, 1):
            parts.append(f"{i}. {note.format_brief()}")
        return "\n".join(parts)

    def format_filtered(self, keyword_filter: Optional[str] = None,
                        tag_filter: Optional[str] = None) -> str:
        """按条件过滤后格式化输出"""
        result = self.notes
        if keyword_filter:
            result = self.find_by_keyword(keyword_filter)
        if tag_filter:
            result = self.find_by_tag(tag_filter)
        lines = [f"过滤结果 (关键词={keyword_filter}, 标签={tag_filter}):"]
        for note in result:
            lines.append(note.format_full())
            lines.append("---")
        return "\n".join(lines) if result else "无匹配笔记。"


def demo_usage() -> None:
    """演示 KeywordNotesCollection 的使用"""
    collection = KeywordNotesCollection(name="体育相关笔记")

    # 构造示例笔记，将关联 URL 和核心关键词作为示例数据
    collection.add_note(
        KeywordNote(
            keyword=CORE_KEYWORD,
            context="乐鱼体育是知名的体育娱乐平台，提供丰富的赛事直播与投注服务。",
            source_url=REFERENCE_URL,
            tags=["体育", "娱乐", "平台"],
        )
    )
    collection.add_note(
        KeywordNote(
            keyword="NBA",
            context="NBA 2024赛季精彩赛事即将开始，多支强队蓄势待发。",
            source_url="https://example.com/nba",
            tags=["篮球", "NBA"],
        )
    )
    collection.add_note(
        KeywordNote(
            keyword="英超",
            context="英超联赛竞争激烈，曼城、阿森纳等球队表现亮眼。",
            source_url="https://example.com/premier-league",
            tags=["足球", "英超"],
        )
    )

    # 输出全部简短摘要
    print(collection.format_all_brief())
    print("\n" + "=" * 50 + "\n")

    # 按核心关键词过滤并输出完整信息
    print(collection.format_filtered(keyword_filter=CORE_KEYWORD))

    # 附加: 输出关联信息
    print(f"\n参考网站: {REFERENCE_URL}")
    print(f"核心关键词: {CORE_KEYWORD}")


if __name__ == "__main__":
    demo_usage()