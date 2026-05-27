import asyncio

from knowledge.knowledge_base import knowledge_base


async def main():

    await knowledge_base.ainsert(
        path="sample.pdf"
    )

    print("PDF inserted successfully!")


asyncio.run(main())