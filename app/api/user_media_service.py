import logging
from ..models.models import ApiResponse


logger = logging.getLogger(__name__)

class UserMediaService:
    def __init__(self, api_client):
        self.api = api_client

    @staticmethod
    def _clean_params(params: dict) -> dict:
        """Remove None values so they don't become 'None' in the query string."""
        return {key: value for key, value in params.items() if value is not None}

    async def get_library(
        self,
        media_type: str,
        status: str | None = None,
        favorite: bool | None = None,
        title: str | None = None,
        year: int | None = None,
        sort_by: str = "created_at",
        order: str = "desc",
        limit: int = 30,
        offset: int = 0,
    ) -> ApiResponse:
        """
        Fetch a paginated list of items in the user's library.

        Maps to: GET /v1/library/
        """
        params = self._clean_params({
            "media_type": media_type,
            "status": status,
            "favorite": favorite,
            "title": title,
            "year": year,
            "sort_by": sort_by,
            "order": order,
            "limit": limit,
            "offset": offset,
        })
        return await self.api.get("library/", params=params)

    async def save_user_media(
        self,
        media_type: str,
        media_id: int,
        **update_data,
    ) -> ApiResponse:
        """
        Upsert user media entry.

        Maps to: POST /v1/library/
        """
        params = {"media_type": media_type, "media_id": media_id}
        return await self.api.post("library/", params=params, json=update_data)

    async def random_pick(
        self,
        media_type: str,
        status: str | None = None,
        favorite: bool | None = None,
    ) -> ApiResponse:
        """
        Get a random item from the user's library.

        Maps to: GET /v1/library/random
        """
        params = self._clean_params({
            "media_type": media_type,
            "status": status,
            "favorite": favorite,
        })
        return await self.api.get("library/random", params=params)

    async def remove_from_list(self, entry_id: int) -> ApiResponse:
        """
        Remove a library entry by its ID.

        Maps to: DELETE /v1/library/{id}
        """
        return await self.api.delete(f"library/{entry_id}")

    async def get_media_details(self, media_type: str, media_id: int) -> ApiResponse:
        """
        Get user media details for a specific media item.

        Maps to: GET /v1/library/{media_type}/{media_id}
        """
        return await self.api.get(f"library/{media_type}/{media_id}")
