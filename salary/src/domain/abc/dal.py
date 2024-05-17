from typing import Generic, TypeVar, List, Any

from beanie import PydanticObjectId
from beanie.odm.operators.update.general import Set


DocumentType = TypeVar('DocumentType')
CreateDTOType = TypeVar('CreateDTOType')
UpdateDTOType = TypeVar('UpdateDTOType')


class DocumentDAO(Generic[DocumentType, CreateDTOType, UpdateDTOType]):
    document: DocumentType = DocumentType
    create_dto: CreateDTOType = CreateDTOType
    update_dto: UpdateDTOType = UpdateDTOType

    @classmethod
    async def create(cls, data_to_insert: CreateDTOType, exclude: set[str] = None, **fields: Any) -> document:
        if exclude is None:
            exclude = {}
        return await cls.document(
            **data_to_insert.model_dump(
                exclude={*exclude, *fields.keys()}, exclude_none=True
            ),
            **fields,
        ).insert()

    @classmethod
    async def update(cls, data_to_update: UpdateDTOType, exclude: set[str] = None, **fields: Any):
        if exclude is None:
            exclude = {}
        await cls.document.find_one(cls.document.id == data_to_update.id).update(
            Set(
                {
                    **data_to_update.model_dump(
                        exclude={*exclude, *fields.keys()}, exclude_none=True, exclude_defaults=True
                    ),
                    **fields
                }
            )
        )

    @classmethod
    async def delete(cls, id_: PydanticObjectId):
        await cls.document.find_one(cls.document.id == id_).delete()

    @classmethod
    async def get_list(cls) -> List[document]:
        return await cls.document.find_all(fetch_links=True).to_list()

    @classmethod
    async def get_by_id(cls, id_: PydanticObjectId) -> document:
        return await cls.document.get(id_)
