import logging
from ..models.models import ApiResponse

logger = logging.getLogger(__name__)


class MediaService:
    MEDIA_TYPES = {"movies", "series", "anime", "games", "manga", "books"}
    MEDIA_TYPE_ALIASES = {
        "movie": "movies",
        "series": "series",
        "anime": "anime",
        "game": "games",
        "manga": "manga",
        "book": "books",
    }
    FROM_API_PARAM = {
        "movies": "tmdb_id",
        "series": "tmdb_id",
        "anime": "mal_id",
        "manga": "mal_id",
        "games": "rawg_id",
        "books": "ol_id",
    }

    def __init__(self, api_client):
        self.api = api_client

    @staticmethod
    def _clean_params(params: dict) -> dict:
        """Remove None values so they don't become 'None' in the query string."""
        return {key: value for key, value in params.items() if value is not None}

    def _normalize_media_type(self, media_type: str) -> str:
        normalized = media_type.strip().strip("/").lower()
        normalized = self.MEDIA_TYPE_ALIASES.get(normalized, normalized)
        return normalized

    def _media_base(self, media_type: str) -> str:
        normalized = self._normalize_media_type(media_type)
        return f"media/{normalized}"

    async def list_media(
        self,
        media_type: str,
        skip: int = 0,
        limit: int = 50,
        genre: str | None = None,
    ) -> ApiResponse:
        """
        List media with pagination and optional genre filter.

        Maps to: GET /v1/media/{media_type}/
        """
        params = self._clean_params({"skip": skip, "limit": limit, "genre": genre})
        return await self.api.get(f"{self._media_base(media_type)}/", params=params)

    async def search_media(
        self,
        media_type: str,
        q: str,
        skip: int = 0,
        limit: int = 10,
    ) -> ApiResponse:
        """
        Search media by title or external IDs.

        Maps to: GET /v1/media/{media_type}/search/
        """
        params = self._clean_params({"q": q, "skip": skip, "limit": limit})
        return await self.api.get(f"{self._media_base(media_type)}/search/", params=params)

    async def get_media(self, media_type: str, media_id: int) -> ApiResponse:
        """
        Get a single media item by ID.

        Maps to: GET /v1/media/{media_type}/{id}
        """
        return await self.api.get(f"{self._media_base(media_type)}/{media_id}")

    async def create_media(self, media_type: str, **data) -> ApiResponse:
        """
        Create a new media item.

        Maps to: POST /v1/media/{media_type}/
        """
        return await self.api.post(f"{self._media_base(media_type)}/", json=data)

    async def update_media(self, media_type: str, media_id: int, **data) -> ApiResponse:
        """
        Update a media item by ID (partial update).

        Maps to: PUT /v1/media/{media_type}/{id}
        """
        return await self.api.put(f"{self._media_base(media_type)}/{media_id}", json=data)

    async def delete_media(self, media_type: str, media_id: int) -> ApiResponse:
        """
        Delete a media item by ID.

        Maps to: DELETE /v1/media/{media_type}/{id}
        """
        return await self.api.delete(f"{self._media_base(media_type)}/{media_id}")

    async def add_from_api(
        self,
        media_type: str,
        external_id: str | int,
        external_id_param: str | None = None,
    ) -> ApiResponse:
        """
        Add a media item by fetching details from an external API.

        Maps to: POST /v1/media/{media_type}/from-api
        """
        normalized = self._normalize_media_type(media_type)
        param_name = external_id_param or self.FROM_API_PARAM.get(normalized)
        if not param_name:
            raise ValueError(
                f"Unknown media_type '{media_type}'. Provide external_id_param explicitly."
            )
        params = {param_name: external_id}
        return await self.api.post(f"{self._media_base(media_type)}/from-api", params=params)
