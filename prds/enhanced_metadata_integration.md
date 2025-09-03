# Enhanced Metadata Integration - External Sources

## 🌐 **External Metadata Sources Integration**

This document outlines the enhanced architecture for pulling metadata from well-known media websites to automatically populate missing information about artists, actors, movies, TV shows, and artwork.

---

## **1. Data Sources Overview**

### **🎵 Audio/Music Sources**

#### **MusicBrainz**
- **API**: Free, comprehensive music database
- **Data**: Artist bios, album info, track listings, genres, release dates
- **Rate Limits**: 1 request per second (can be optimized with caching)
- **Coverage**: Global music database with 2M+ artists

#### **Discogs**
- **API**: Free tier with rate limits
- **Data**: Release info, genres, styles, artist bios, album artwork
- **Rate Limits**: 60 requests per minute
- **Coverage**: Extensive electronic, jazz, and alternative music

#### **Last.fm**
- **API**: Free with API key
- **Data**: Music recommendations, similar artists, tags, user ratings
- **Rate Limits**: 10 requests per second
- **Coverage**: User-generated content and recommendations

#### **Spotify Web API**
- **API**: Free with OAuth authentication
- **Data**: Artist info, genres, popularity, related artists, album artwork
- **Rate Limits**: 25 requests per second
- **Coverage**: Current music with high-quality metadata

#### **iTunes Search API**
- **API**: Free, no authentication required
- **Data**: Album artwork, reviews, ratings, genre classification
- **Rate Limits**: No strict limits
- **Coverage**: Popular music with high-quality artwork

### **🎬 Video/Movie Sources**

#### **The Movie Database (TMDB)**
- **API**: Free with API key
- **Data**: Movies, TV shows, cast, crew, posters, backdrops, trailers
- **Rate Limits**: 40 requests per 10 seconds
- **Coverage**: Comprehensive movie/TV database

#### **Open Movie Database (OMDB)**
- **API**: Free with API key
- **Data**: Movie ratings, plot summaries, awards, box office data
- **Rate Limits**: 1000 requests per day
- **Coverage**: Movies and TV shows with ratings

#### **IMDb**
- **API**: Limited free access, paid options available
- **Data**: Comprehensive movie/TV database, cast, crew, ratings
- **Rate Limits**: Varies by plan
- **Coverage**: Most comprehensive movie database

#### **TVDB**
- **API**: Free with API key
- **Data**: Television series information, episodes, cast
- **Rate Limits**: 5 requests per second
- **Coverage**: TV series focus

#### **Fanart.tv**
- **API**: Free with API key
- **Data**: High-quality movie/TV artwork, posters, backgrounds
- **Rate Limits**: 1000 requests per day
- **Coverage**: High-quality artwork for movies/TV

### **🖼️ Image/Artwork Sources**

#### **Google Images API**
- **API**: Free with API key
- **Data**: Album covers, movie posters, artist photos
- **Rate Limits**: 100 requests per day
- **Coverage**: Extensive image database

#### **Bing Image Search**
- **API**: Free with API key
- **Data**: Alternative image source for covers and posters
- **Rate Limits**: 1000 requests per month
- **Coverage**: Good alternative to Google

#### **Wikipedia**
- **API**: Free, no authentication required
- **Data**: Public domain images, artist bios, movie information
- **Rate Limits**: No strict limits
- **Coverage**: Public domain content

#### **Flickr**
- **API**: Free with API key
- **Data**: Creative Commons licensed images
- **Rate Limits**: 1000 requests per day
- **Coverage**: Creative Commons artwork

---

## **2. Enhanced Project Structure**

```
media_file_manager/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── file_processor.py
│   │   ├── metadata_handler.py
│   │   ├── file_renamer.py
│   │   └── validator.py
│   ├── media/
│   │   ├── __init__.py
│   │   ├── audio_processor.py
│   │   ├── video_processor.py
│   │   └── format_detector.py
│   ├── metadata_sources/           # NEW: External metadata sources
│   │   ├── __init__.py
│   │   ├── base_source.py          # Abstract base class
│   │   ├── music/
│   │   │   ├── __init__.py
│   │   │   ├── musicbrainz.py
│   │   │   ├── discogs.py
│   │   │   ├── lastfm.py
│   │   │   ├── spotify.py
│   │   │   └── itunes.py
│   │   ├── video/
│   │   │   ├── __init__.py
│   │   │   ├── tmdb.py
│   │   │   ├── omdb.py
│   │   │   ├── imdb.py
│   │   │   ├── tvdb.py
│   │   │   └── fanart.py
│   │   ├── images/
│   │   │   ├── __init__.py
│   │   │   ├── google_images.py
│   │   │   ├── bing_images.py
│   │   │   ├── wikipedia.py
│   │   │   └── flickr.py
│   │   └── aggregator.py           # Combines multiple sources
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── logger.py
│   │   ├── file_utils.py
│   │   ├── backup.py
│   │   ├── cache.py                # NEW: API response caching
│   │   ├── rate_limiter.py         # NEW: API rate limiting
│   │   └── image_processor.py      # NEW: Image processing utilities
│   └── cli/
│       ├── __init__.py
│       ├── commands.py
│       └── interface.py
├── config/
│   ├── default_config.yaml
│   ├── user_config.yaml
│   └── api_keys.yaml               # NEW: API keys configuration
├── cache/                           # NEW: Local cache directory
│   ├── api_responses/
│   ├── images/
│   └── metadata/
└── docs/
    ├── README.md
    ├── API.md
    ├── USER_GUIDE.md
    └── METADATA_SOURCES.md          # NEW: External sources documentation
```

---

## **3. Core Components Implementation**

### **3.1 Base Metadata Source (`src/metadata_sources/base_source.py`)**

```python
"""
Base class for all external metadata sources.

This abstract base class defines the interface that all metadata
sources must implement for consistency and interoperability.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from pathlib import Path
import logging
import time
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class SearchResult:
    """Result from metadata source search."""
    source_name: str
    confidence: float  # 0.0 to 1.0
    metadata: Dict[str, Any]
    artwork_urls: List[str]
    raw_response: Dict[str, Any]


@dataclass
class MetadataSourceConfig:
    """Configuration for a metadata source."""
    enabled: bool = True
    api_key: Optional[str] = None
    rate_limit: Optional[int] = None
    cache_duration: int = 3600  # seconds
    priority: int = 1  # Higher number = higher priority


class BaseMetadataSource(ABC):
    """
    Abstract base class for metadata sources.
    
    All external metadata sources must inherit from this class
    and implement the required methods.
    """
    
    def __init__(self, config: MetadataSourceConfig):
        """Initialize the metadata source with configuration."""
        self.config = config
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.last_request_time = 0
        
    @abstractmethod
    def search_audio(self, query: str, **kwargs) -> List[SearchResult]:
        """
        Search for audio metadata.
        
        Args:
            query: Search query (artist, title, album)
            **kwargs: Additional search parameters
            
        Returns:
            List of search results
        """
        pass
        
    @abstractmethod
    def search_video(self, query: str, **kwargs) -> List[SearchResult]:
        """
        Search for video metadata.
        
        Args:
            query: Search query (title, year, director)
            **kwargs: Additional search parameters
            
        Returns:
            List of search results
        """
        pass
        
    @abstractmethod
    def get_artwork(self, identifier: str, **kwargs) -> List[str]:
        """
        Get artwork URLs for a media item.
        
        Args:
            identifier: Unique identifier for the media item
            **kwargs: Additional parameters
            
        Returns:
            List of artwork URLs
        """
        pass
        
    def _rate_limit(self) -> None:
        """Implement rate limiting for API requests."""
        if self.config.rate_limit:
            time_since_last = time.time() - self.last_request_time
            min_interval = 1.0 / self.config.rate_limit
            
            if time_since_last < min_interval:
                sleep_time = min_interval - time_since_last
                time.sleep(sleep_time)
                
        self.last_request_time = time.time()
        
    def _validate_response(self, response: Dict[str, Any]) -> bool:
        """Validate API response format."""
        # Implement basic response validation
        return isinstance(response, dict) and len(response) > 0
        
    def _extract_common_metadata(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Extract common metadata fields from API response."""
        # Implement common metadata extraction logic
        metadata = {}
        
        # Common fields that most sources provide
        common_fields = ['title', 'year', 'genre', 'description', 'rating']
        
        for field in common_fields:
            if field in response:
                metadata[field] = response[field]
                
        return metadata
```

### **3.2 MusicBrainz Integration (`src/metadata_sources/music/musicbrainz.py`)**

```python
"""
MusicBrainz metadata source integration.

MusicBrainz is a comprehensive music database that provides
detailed information about artists, albums, and tracks.
"""

import requests
from typing import Dict, List, Optional, Any
from ..base_source import BaseMetadataSource, SearchResult, MetadataSourceConfig
import logging

logger = logging.getLogger(__name__)


class MusicBrainzSource(BaseMetadataSource):
    """MusicBrainz metadata source implementation."""
    
    def __init__(self, config: MetadataSourceConfig):
        """Initialize MusicBrainz source."""
        super().__init__(config)
        self.base_url = "https://musicbrainz.org/ws/2"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'MediaFileManager/1.0.0 (your-email@example.com)'
        })
        
    def search_audio(self, query: str, **kwargs) -> List[SearchResult]:
        """
        Search for audio metadata using MusicBrainz.
        
        Args:
            query: Search query (artist, title, album)
            **kwargs: Additional search parameters
            
        Returns:
            List of search results
        """
        self._rate_limit()
        
        try:
            # Search for recordings
            search_params = {
                'query': query,
                'fmt': 'json',
                'limit': 10
            }
            
            response = self.session.get(
                f"{self.base_url}/recording/",
                params=search_params
            )
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            for recording in data.get('recordings', []):
                # Extract basic recording info
                metadata = {
                    'title': recording.get('title'),
                    'artist': self._extract_artist(recording),
                    'album': self._extract_album(recording),
                    'year': self._extract_year(recording),
                    'genre': self._extract_genres(recording),
                    'mbid': recording.get('id'),
                    'length': recording.get('length'),
                    'tags': [tag['name'] for tag in recording.get('tags', [])]
                }
                
                # Calculate confidence based on match quality
                confidence = self._calculate_confidence(query, metadata)
                
                result = SearchResult(
                    source_name="MusicBrainz",
                    confidence=confidence,
                    metadata=metadata,
                    artwork_urls=[],  # MusicBrainz doesn't provide artwork
                    raw_response=recording
                )
                
                results.append(result)
                
            return sorted(results, key=lambda x: x.confidence, reverse=True)
            
        except Exception as e:
            self.logger.error(f"MusicBrainz search failed: {e}")
            return []
            
    def search_video(self, query: str, **kwargs) -> List[SearchResult]:
        """MusicBrainz doesn't support video content."""
        return []
        
    def get_artwork(self, identifier: str, **kwargs) -> List[str]:
        """MusicBrainz doesn't provide artwork directly."""
        return []
        
    def _extract_artist(self, recording: Dict[str, Any]) -> Optional[str]:
        """Extract artist name from recording data."""
        artists = recording.get('artist-credit', [])
        if artists:
            return artists[0].get('name')
        return None
        
    def _extract_album(self, recording: Dict[str, Any]) -> Optional[str]:
        """Extract album name from recording data."""
        releases = recording.get('releases', [])
        if releases:
            return releases[0].get('title')
        return None
        
    def _extract_year(self, recording: Dict[str, Any]) -> Optional[int]:
        """Extract release year from recording data."""
        releases = recording.get('releases', [])
        if releases:
            date = releases[0].get('date')
            if date:
                try:
                    return int(date[:4])
                except (ValueError, IndexError):
                    pass
        return None
        
    def _extract_genres(self, recording: Dict[str, Any]) -> List[str]:
        """Extract genres from recording data."""
        genres = []
        for tag in recording.get('tags', []):
            if tag.get('count', 0) > 1:  # Only include tags with multiple votes
                genres.append(tag['name'])
        return genres
        
    def _calculate_confidence(self, query: str, metadata: Dict[str, Any]) -> float:
        """Calculate confidence score for search result."""
        confidence = 0.0
        
        # Title match
        if metadata.get('title'):
            if query.lower() in metadata['title'].lower():
                confidence += 0.4
            elif metadata['title'].lower() in query.lower():
                confidence += 0.3
                
        # Artist match
        if metadata.get('artist'):
            if query.lower() in metadata['artist'].lower():
                confidence += 0.3
                
        # Album match
        if metadata.get('album'):
            if query.lower() in metadata['album'].lower():
                confidence += 0.2
                
        # Genre tags
        if metadata.get('tags'):
            confidence += min(len(metadata['tags']) * 0.05, 0.1)
            
        return min(confidence, 1.0)
```

### **3.3 TMDB Integration (`src/metadata_sources/video/tmdb.py`)**

```python
"""
The Movie Database (TMDB) metadata source integration.

TMDB provides comprehensive information about movies and TV shows
including cast, crew, posters, and detailed metadata.
"""

import requests
from typing import Dict, List, Optional, Any
from ..base_source import BaseMetadataSource, SearchResult, MetadataSourceConfig
import logging

logger = logging.getLogger(__name__)


class TMDBSource(BaseMetadataSource):
    """TMDB metadata source implementation."""
    
    def __init__(self, config: MetadataSourceConfig):
        """Initialize TMDB source."""
        super().__init__(config)
        if not self.config.api_key:
            raise ValueError("TMDB requires an API key")
            
        self.base_url = "https://api.themoviedb.org/3"
        self.api_key = self.config.api_key
        self.session = requests.Session()
        
    def search_audio(self, query: str, **kwargs) -> List[SearchResult]:
        """TMDB doesn't support audio content."""
        return []
        
    def search_video(self, query: str, **kwargs) -> List[SearchResult]:
        """
        Search for video metadata using TMDB.
        
        Args:
            query: Search query (title, year, director)
            **kwargs: Additional search parameters
            
        Returns:
            List of search results
        """
        self._rate_limit()
        
        try:
            # Search for movies
            movie_results = self._search_movies(query, **kwargs)
            
            # Search for TV shows
            tv_results = self._search_tv_shows(query, **kwargs)
            
            # Combine and sort results
            all_results = movie_results + tv_results
            return sorted(all_results, key=lambda x: x.confidence, reverse=True)
            
        except Exception as e:
            self.logger.error(f"TMDB search failed: {e}")
            return []
            
    def get_artwork(self, identifier: str, **kwargs) -> List[str]:
        """
        Get artwork URLs for a media item.
        
        Args:
            identifier: TMDB ID for the movie/TV show
            **kwargs: Additional parameters
            
        Returns:
            List of artwork URLs
        """
        self._rate_limit()
        
        try:
            media_type = kwargs.get('media_type', 'movie')
            
            if media_type == 'movie':
                return self._get_movie_artwork(identifier)
            elif media_type == 'tv':
                return self._get_tv_artwork(identifier)
            else:
                return []
                
        except Exception as e:
            self.logger.error(f"TMDB artwork fetch failed: {e}")
            return []
            
    def _search_movies(self, query: str, **kwargs) -> List[SearchResult]:
        """Search for movies in TMDB."""
        search_params = {
            'api_key': self.api_key,
            'query': query,
            'language': 'en-US',
            'page': 1,
            'include_adult': False
        }
        
        response = self.session.get(
            f"{self.base_url}/search/movie",
            params=search_params
        )
        response.raise_for_status()
        
        data = response.json()
        results = []
        
        for movie in data.get('results', []):
            metadata = {
                'title': movie.get('title'),
                'original_title': movie.get('original_title'),
                'year': self._extract_year(movie.get('release_date')),
                'overview': movie.get('overview'),
                'genre_ids': movie.get('genre_ids', []),
                'rating': movie.get('vote_average'),
                'vote_count': movie.get('vote_count'),
                'popularity': movie.get('popularity'),
                'poster_path': movie.get('poster_path'),
                'backdrop_path': movie.get('backdrop_path'),
                'tmdb_id': movie.get('id'),
                'media_type': 'movie'
            }
            
            # Get detailed movie info
            detailed_metadata = self._get_movie_details(movie.get('id'))
            metadata.update(detailed_metadata)
            
            confidence = self._calculate_confidence(query, metadata)
            
            result = SearchResult(
                source_name="TMDB",
                confidence=confidence,
                metadata=metadata,
                artwork_urls=self._get_artwork_urls(metadata),
                raw_response=movie
            )
            
            results.append(result)
            
        return results
        
    def _search_tv_shows(self, query: str, **kwargs) -> List[SearchResult]:
        """Search for TV shows in TMDB."""
        search_params = {
            'api_key': self.api_key,
            'query': query,
            'language': 'en-US',
            'page': 1,
            'include_adult': False
        }
        
        response = self.session.get(
            f"{self.base_url}/search/tv",
            params=search_params
        )
        response.raise_for_status()
        
        data = response.json()
        results = []
        
        for tv_show in data.get('results', []):
            metadata = {
                'title': tv_show.get('name'),
                'original_title': tv_show.get('original_name'),
                'year': self._extract_year(tv_show.get('first_air_date')),
                'overview': tv_show.get('overview'),
                'genre_ids': tv_show.get('genre_ids', []),
                'rating': tv_show.get('vote_average'),
                'vote_count': tv_show.get('vote_count'),
                'popularity': tv_show.get('popularity'),
                'poster_path': tv_show.get('poster_path'),
                'backdrop_path': tv_show.get('backdrop_path'),
                'tmdb_id': tv_show.get('id'),
                'media_type': 'tv'
            }
            
            # Get detailed TV show info
            detailed_metadata = self._get_tv_details(tv_show.get('id'))
            metadata.update(detailed_metadata)
            
            confidence = self._calculate_confidence(query, metadata)
            
            result = SearchResult(
                source_name="TMDB",
                confidence=confidence,
                metadata=metadata,
                artwork_urls=self._get_artwork_urls(metadata),
                raw_response=tv_show
            )
            
            results.append(result)
            
        return results
        
    def _get_movie_details(self, movie_id: int) -> Dict[str, Any]:
        """Get detailed movie information."""
        try:
            response = self.session.get(
                f"{self.base_url}/movie/{movie_id}",
                params={'api_key': self.api_key}
            )
            response.raise_for_status()
            
            data = response.json()
            
            return {
                'genres': [genre['name'] for genre in data.get('genres', [])],
                'runtime': data.get('runtime'),
                'budget': data.get('budget'),
                'revenue': data.get('revenue'),
                'status': data.get('status'),
                'production_companies': [
                    company['name'] for company in data.get('production_companies', [])
                ]
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get movie details: {e}")
            return {}
            
    def _get_tv_details(self, tv_id: int) -> Dict[str, Any]:
        """Get detailed TV show information."""
        try:
            response = self.session.get(
                f"{self.base_url}/tv/{tv_id}",
                params={'api_key': self.api_key}
            )
            response.raise_for_status()
            
            data = response.json()
            
            return {
                'genres': [genre['name'] for genre in data.get('genres', [])],
                'episode_run_time': data.get('episode_run_time'),
                'number_of_seasons': data.get('number_of_seasons'),
                'number_of_episodes': data.get('number_of_episodes'),
                'status': data.get('status'),
                'production_companies': [
                    company['name'] for company in data.get('production_companies', [])
                ]
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get TV details: {e}")
            return {}
            
    def _get_artwork_urls(self, metadata: Dict[str, Any]) -> List[str]:
        """Get artwork URLs from metadata."""
        base_url = "https://image.tmdb.org/t/p/original"
        urls = []
        
        if metadata.get('poster_path'):
            urls.append(f"{base_url}{metadata['poster_path']}")
            
        if metadata.get('backdrop_path'):
            urls.append(f"{base_url}{metadata['backdrop_path']}")
            
        return urls
        
    def _extract_year(self, date_string: Optional[str]) -> Optional[int]:
        """Extract year from date string."""
        if date_string:
            try:
                return int(date_string[:4])
            except (ValueError, IndexError):
                pass
        return None
        
    def _calculate_confidence(self, query: str, metadata: Dict[str, Any]) -> float:
        """Calculate confidence score for search result."""
        confidence = 0.0
        
        # Title match
        title = metadata.get('title', '').lower()
        query_lower = query.lower()
        
        if query_lower in title:
            confidence += 0.5
        elif title in query_lower:
            confidence += 0.4
            
        # Year match (if provided in query)
        if metadata.get('year'):
            confidence += 0.2
            
        # Rating/popularity boost
        if metadata.get('rating', 0) > 7.0:
            confidence += 0.1
            
        if metadata.get('popularity', 0) > 100:
            confidence += 0.1
            
        # Genre match (if query contains genre terms)
        genres = [g.lower() for g in metadata.get('genres', [])]
        genre_terms = ['action', 'comedy', 'drama', 'horror', 'sci-fi', 'romance']
        
        for term in genre_terms:
            if term in query_lower and term in genres:
                confidence += 0.1
                
        return min(confidence, 1.0)
```

### **3.4 Metadata Aggregator (`src/metadata_sources/aggregator.py`)**

```python
"""
Metadata aggregator that combines results from multiple sources.

This module intelligently combines metadata from various sources
to provide the most complete and accurate information.
"""

from typing import Dict, List, Optional, Any
from .base_source import SearchResult, MetadataSourceConfig
from .music import MusicBrainzSource, DiscogsSource, LastFMSource, SpotifySource, iTunesSource
from .video import TMDBSource, OMDBSource, IMDBSource, TVDBSource, FanartSource
from .images import GoogleImagesSource, BingImagesSource, WikipediaSource, FlickrSource
import logging

logger = logging.getLogger(__name__)


class MetadataAggregator:
    """
    Aggregates metadata from multiple sources.
    
    This class intelligently combines results from various metadata
    sources to provide comprehensive information about media files.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the metadata aggregator."""
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Initialize metadata sources
        self.audio_sources = self._initialize_audio_sources()
        self.video_sources = self._initialize_video_sources()
        self.image_sources = self._initialize_image_sources()
        
    def search_audio_metadata(self, query: str, **kwargs) -> Dict[str, Any]:
        """
        Search for audio metadata across all sources.
        
        Args:
            query: Search query (artist, title, album)
            **kwargs: Additional search parameters
            
        Returns:
            Aggregated metadata dictionary
        """
        self.logger.info(f"Searching audio metadata for: {query}")
        
        all_results = []
        
        # Search all audio sources
        for source in self.audio_sources:
            try:
                results = source.search_audio(query, **kwargs)
                all_results.extend(results)
            except Exception as e:
                self.logger.error(f"Error searching {source.__class__.__name__}: {e}")
                
        # Aggregate and rank results
        aggregated_metadata = self._aggregate_audio_results(all_results, query)
        
        # Enhance with artwork
        if aggregated_metadata.get('title') and aggregated_metadata.get('artist'):
            artwork_urls = self._search_audio_artwork(
                aggregated_metadata['title'],
                aggregated_metadata['artist']
            )
            aggregated_metadata['artwork_urls'] = artwork_urls
            
        return aggregated_metadata
        
    def search_video_metadata(self, query: str, **kwargs) -> Dict[str, Any]:
        """
        Search for video metadata across all sources.
        
        Args:
            query: Search query (title, year, director)
            **kwargs: Additional search parameters
            
        Returns:
            Aggregated metadata dictionary
        """
        self.logger.info(f"Searching video metadata for: {query}")
        
        all_results = []
        
        # Search all video sources
        for source in self.video_sources:
            try:
                results = source.search_video(query, **kwargs)
                all_results.extend(results)
            except Exception as e:
                self.logger.error(f"Error searching {source.__class__.__name__}: {e}")
                
        # Aggregate and rank results
        aggregated_metadata = self._aggregate_video_results(all_results, query)
        
        # Enhance with artwork
        if aggregated_metadata.get('title'):
            artwork_urls = self._search_video_artwork(
                aggregated_metadata['title'],
                aggregated_metadata.get('year')
            )
            aggregated_metadata['artwork_urls'] = artwork_urls
            
        return aggregated_metadata
        
    def _initialize_audio_sources(self) -> List:
        """Initialize audio metadata sources."""
        sources = []
        
        # MusicBrainz (always enabled)
        sources.append(MusicBrainzSource(MetadataSourceConfig(enabled=True)))
        
        # Other sources based on configuration
        if self.config.get('metadata_sources', {}).get('discogs', {}).get('enabled', False):
            sources.append(DiscogsSource(MetadataSourceConfig(
                enabled=True,
                api_key=self.config['metadata_sources']['discogs'].get('api_key')
            )))
            
        if self.config.get('metadata_sources', {}).get('lastfm', {}).get('enabled', False):
            sources.append(LastFMSource(MetadataSourceConfig(
                enabled=True,
                api_key=self.config['metadata_sources']['lastfm'].get('api_key')
            )))
            
        if self.config.get('metadata_sources', {}).get('spotify', {}).get('enabled', False):
            sources.append(SpotifySource(MetadataSourceConfig(
                enabled=True,
                api_key=self.config['metadata_sources']['spotify'].get('api_key')
            )))
            
        if self.config.get('metadata_sources', {}).get('itunes', {}).get('enabled', False):
            sources.append(iTunesSource(MetadataSourceConfig(enabled=True)))
            
        return sources
        
    def _initialize_video_sources(self) -> List:
        """Initialize video metadata sources."""
        sources = []
        
        # TMDB (if API key provided)
        if self.config.get('metadata_sources', {}).get('tmdb', {}).get('api_key'):
            sources.append(TMDBSource(MetadataSourceConfig(
                enabled=True,
                api_key=self.config['metadata_sources']['tmdb']['api_key']
            )))
            
        # OMDB (if API key provided)
        if self.config.get('metadata_sources', {}).get('omdb', {}).get('api_key'):
            sources.append(OMDBSource(MetadataSourceConfig(
                enabled=True,
                api_key=self.config['metadata_sources']['omdb']['api_key']
            )))
            
        # Other sources based on configuration
        if self.config.get('metadata_sources', {}).get('imdb', {}).get('enabled', False):
            sources.append(IMDBSource(MetadataSourceConfig(
                enabled=True,
                api_key=self.config['metadata_sources']['imdb'].get('api_key')
            )))
            
        return sources
        
    def _initialize_image_sources(self) -> List:
        """Initialize image sources."""
        sources = []
        
        # Google Images (if API key provided)
        if self.config.get('metadata_sources', {}).get('google_images', {}).get('api_key'):
            sources.append(GoogleImagesSource(MetadataSourceConfig(
                enabled=True,
                api_key=self.config['metadata_sources']['google_images']['api_key']
            )))
            
        # Other image sources
        if self.config.get('metadata_sources', {}).get('wikipedia', {}).get('enabled', True):
            sources.append(WikipediaSource(MetadataSourceConfig(enabled=True)))
            
        return sources
        
    def _aggregate_audio_results(self, results: List[SearchResult], query: str) -> Dict[str, Any]:
        """Aggregate audio metadata results."""
        if not results:
            return {}
            
        # Sort by confidence and source priority
        sorted_results = sorted(
            results,
            key=lambda x: (x.confidence, x.source_name),
            reverse=True
        )
        
        # Start with the highest confidence result
        best_result = sorted_results[0]
        aggregated = best_result.metadata.copy()
        
        # Enhance with additional information from other sources
        for result in sorted_results[1:]:
            if result.confidence > 0.7:  # Only use high-confidence results
                self._merge_metadata(aggregated, result.metadata)
                
        return aggregated
        
    def _aggregate_video_results(self, results: List[SearchResult], query: str) -> Dict[str, Any]:
        """Aggregate video metadata results."""
        if not results:
            return {}
            
        # Sort by confidence and source priority
        sorted_results = sorted(
            results,
            key=lambda x: (x.confidence, x.source_name),
            reverse=True
        )
        
        # Start with the highest confidence result
        best_result = sorted_results[0]
        aggregated = best_result.metadata.copy()
        
        # Enhance with additional information from other sources
        for result in sorted_results[1:]:
            if result.confidence > 0.7:  # Only use high-confidence results
                self._merge_metadata(aggregated, result.metadata)
                
        return aggregated
        
    def _merge_metadata(self, base: Dict[str, Any], additional: Dict[str, Any]) -> None:
        """Merge additional metadata into base metadata."""
        for key, value in additional.items():
            if key not in base or not base[key]:
                base[key] = value
            elif isinstance(base[key], list) and isinstance(value, list):
                # Merge lists, avoiding duplicates
                base[key].extend([v for v in value if v not in base[key]])
            elif isinstance(base[key], str) and isinstance(value, str):
                # Keep the longer/more detailed string
                if len(value) > len(base[key]):
                    base[key] = value
                    
    def _search_audio_artwork(self, title: str, artist: str) -> List[str]:
        """Search for audio artwork."""
        query = f"{artist} {title} album cover"
        artwork_urls = []
        
        for source in self.image_sources:
            try:
                urls = source.get_artwork(query)
                artwork_urls.extend(urls)
            except Exception as e:
                self.logger.error(f"Error getting artwork from {source.__class__.__name__}: {e}")
                
        return artwork_urls[:5]  # Limit to 5 results
        
    def _search_video_artwork(self, title: str, year: Optional[int] = None) -> List[str]:
        """Search for video artwork."""
        query = f"{title}"
        if year:
            query += f" {year}"
        query += " movie poster"
        
        artwork_urls = []
        
        for source in self.image_sources:
            try:
                urls = source.get_artwork(query)
                artwork_urls.extend(urls)
            except Exception as e:
                self.logger.error(f"Error getting artwork from {source.__class__.__name__}: {e}")
                
        return artwork_urls[:5]  # Limit to 5 results
```

---

## **4. Configuration Updates**

### **4.1 API Keys Configuration (`config/api_keys.yaml`)**

```yaml
# API Keys for External Metadata Sources
# Copy this file to api_keys.yaml and add your actual API keys

metadata_sources:
  # Music Sources
  musicbrainz:
    enabled: true
    # MusicBrainz is free and doesn't require an API key
    
  discogs:
    enabled: false
    api_key: "YOUR_DISCOGS_API_KEY"
    
  lastfm:
    enabled: false
    api_key: "YOUR_LASTFM_API_KEY"
    
  spotify:
    enabled: false
    client_id: "YOUR_SPOTIFY_CLIENT_ID"
    client_secret: "YOUR_SPOTIFY_CLIENT_SECRET"
    
  itunes:
    enabled: true
    # iTunes Search API is free
    
  # Video Sources
  tmdb:
    enabled: false
    api_key: "YOUR_TMDB_API_KEY"
    
  omdb:
    enabled: false
    api_key: "YOUR_OMDB_API_KEY"
    
  imdb:
    enabled: false
    api_key: "YOUR_IMDB_API_KEY"
    
  tvdb:
    enabled: false
    api_key: "YOUR_TVDB_API_KEY"
    
  fanart:
    enabled: false
    api_key: "YOUR_FANART_API_KEY"
    
  # Image Sources
  google_images:
    enabled: false
    api_key: "YOUR_GOOGLE_API_KEY"
    custom_search_engine_id: "YOUR_CUSTOM_SEARCH_ENGINE_ID"
    
  bing_images:
    enabled: false
    api_key: "YOUR_BING_API_KEY"
    
  wikipedia:
    enabled: true
    # Wikipedia API is free
    
  flickr:
    enabled: false
    api_key: "YOUR_FLICKR_API_KEY"
```

### **4.2 Enhanced User Configuration (`config/user_config.yaml`)**

```yaml
# Enhanced User Configuration with External Metadata Sources

# Metadata source preferences
metadata_sources:
  # Priority order for metadata sources
  audio_priority: ["musicbrainz", "discogs", "lastfm", "spotify", "itunes"]
  video_priority: ["tmdb", "omdb", "imdb", "tvdb", "fanart"]
  image_priority: ["google_images", "wikipedia", "flickr"]
  
  # Automatic metadata enhancement
  auto_enhance: true
  enhance_threshold: 0.7  # Minimum confidence for enhancement
  
  # Artwork preferences
  artwork:
    download_automatically: true
    preferred_sizes: ["original", "large", "medium"]
    max_downloads: 5
    save_locally: true
    local_directory: "~/media_artwork"
    
  # Caching preferences
  caching:
    enabled: true
    cache_duration: 86400  # 24 hours in seconds
    max_cache_size: "1GB"
    
  # Rate limiting
  rate_limiting:
    enabled: true
    requests_per_minute: 60
    delay_between_requests: 1.0  # seconds

# Enhanced naming patterns with metadata placeholders
naming:
  audio_pattern: "{artist} - {title} ({year}) [{genre}]"
  video_pattern: "{title} ({year}) [{quality}] [{genre}]"
  
# Metadata field preferences
metadata:
  audio:
    required_fields: ["artist", "title", "album", "year"]
    optional_fields: ["genre", "track", "bpm", "key", "composer", "lyrics", "artwork"]
    auto_fill_missing: true
    
  video:
    required_fields: ["title", "year"]
    optional_fields: ["genre", "director", "cast", "description", "rating", "artwork"]
    auto_fill_missing: true
```

---

## **5. Usage Examples**

### **5.1 Enhanced CLI Commands**

```bash
# Search and enhance metadata for audio files
media-manager enhance-audio "path/to/music" --auto-fill --download-artwork

# Search and enhance metadata for video files
media-manager enhance-video "path/to/movies" --auto-fill --download-posters

# Search specific metadata
media-manager search "The Beatles - Hey Jude" --sources musicbrainz,spotify

# Download artwork for existing files
media-manager download-artwork "path/to/files" --sources google,wikipedia
```

### **5.2 Python API Usage**

```python
from media_file_manager.metadata_sources.aggregator import MetadataAggregator

# Initialize aggregator
aggregator = MetadataAggregator(config)

# Search for audio metadata
audio_metadata = aggregator.search_audio_metadata("The Beatles - Hey Jude")

# Search for video metadata
video_metadata = aggregator.search_video_metadata("The Matrix 1999")

# Print results
print(f"Audio: {audio_metadata['title']} by {audio_metadata['artist']}")
print(f"Video: {video_metadata['title']} ({video_metadata['year']})")
print(f"Artwork URLs: {audio_metadata.get('artwork_urls', [])}")
```

---

## **6. Implementation Benefits**

### **🎯 Automatic Metadata Population**
- **Fill Missing Fields**: Automatically populate artist, album, year, genre
- **Enhanced Information**: Add BPM, key, composer, lyrics for music
- **Cast & Crew**: Add director, cast, plot summaries for videos
- **Ratings & Reviews**: Include user ratings and critical reviews

### **🖼️ High-Quality Artwork**
- **Album Covers**: Download high-resolution album artwork
- **Movie Posters**: Get official movie posters and backdrops
- **Multiple Sources**: Combine results from multiple image sources
- **Local Storage**: Cache artwork locally for offline use

### **🔍 Intelligent Search**
- **Fuzzy Matching**: Handle typos and variations in titles
- **Confidence Scoring**: Rank results by accuracy
- **Source Aggregation**: Combine information from multiple sources
- **Fallback Sources**: Use alternative sources if primary fails

### **⚡ Performance & Reliability**
- **Smart Caching**: Cache API responses to reduce API calls
- **Rate Limiting**: Respect API rate limits automatically
- **Error Handling**: Graceful fallback when sources fail
- **Offline Support**: Work with cached data when offline

---

## **7. Next Steps**

1. **API Key Setup**: Get API keys from the services you want to use
2. **Source Implementation**: Implement the metadata source classes
3. **Testing**: Test with real media files and various metadata scenarios
4. **Integration**: Integrate with the existing file processing pipeline
5. **User Interface**: Add CLI commands for metadata enhancement

This enhanced system will transform your Media File Manager from a basic file organizer into a comprehensive media intelligence tool that automatically enriches your media library with rich metadata and artwork from the web! 🚀
