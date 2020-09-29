#!/usr/bin/env python3

"""EGL configuration management for Pegl."""

# Copyright © 2012, 2020 Tim Pederick.
#
# This file is part of Pegl.
#
# Pegl is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pegl is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public
# License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Pegl. If not, see <http://www.gnu.org/licenses/>.

from __future__ import annotations

__all__ = ['Config']

# Standard library imports.
from typing import Any, Optional

# Local imports.
from . import egl
from .attribs import attrib_list
from ._caching import Cached
from .enums import ConfigCaveat, SurfaceTypeFlag, TransparentType
from .context import Context
from .surface import Surface

# TODO: The value of an EGLConfig is not the same as its ID, as retrieved by
# config_id (on the config or on a surface created from it). This complicates
# caching quite a bit... And it's entirely possible that it affects other
# cached types as well!

class Config(Cached):
    """A set of EGL configuration options."""
    def __init__(self, display: Display, handle: Any):
        self._display = display
        self._as_parameter_ = handle

        self.__class__._add_to_cache(self)

    def create_context(self, share_context: Optional[Context]=None,
                       attribs: Optional[dict[ContextAttrib, Any]]=None
                       ) -> Context:
        """Create a rendering context that uses this configuration."""
        return Context(self._display,
                       egl.eglCreateContext(self._display, self,
                                            egl.EGL_NO_CONTEXT if share_context
                                            is None else share_context,
                                            attrib_list(attribs)))

    def create_pbuffer_surface(self,
                               attribs: Optional[dict[SurfaceAttrib,
                                                      Any]]=None) -> Surface:
        """Create a pbuffer (off-screen) rendering surface."""
        return Surface(self._display,
                       egl.eglCreatePbufferSurface(self._display, self,
                                                   attrib_list(attribs)))

    def create_pixmap_surface(self, pixmap: int,
                              attribs: Optional[dict[SurfaceAttrib,
                                                     Any]]=None) -> Surface:
        """Create a pixmap (off-screen) rendering surface."""
        return Surface(self._display,
                       egl.eglCreatePixmapSurface(self._display, self, pixmap,
                                                  attrib_list(attribs)))

    def create_window_surface(self, win: int,
                              attribs: Optional[dict[SurfaceAttrib, Any]]=None
                              ) -> Surface:
        """Create a window (on-screen) rendering surface."""
        return Surface(self._display,
                       egl.eglCreateWindowSurface(self._display, self, win,
                                                  attrib_list(attribs)))

    def get_config_attrib(self, attribute: ConfigAttrib) -> int:
        """Get an attribute of this configuration.

        Users will generally not need this function, as the available
        attributes may be queried using properties instead.

        """
        return egl.eglGetConfigAttrib(self._display, self, attribute)

    @property
    def alpha_size(self) -> int:
        """The number of color buffer bits used for alpha."""
        return egl.eglGetConfigAttrib(self._display, self, egl.EGL_ALPHA_SIZE)

    @property
    def blue_size(self) -> int:
        """The number of color buffer bits used for blue."""
        return egl.eglGetConfigAttrib(self._display, self, egl.EGL_BLUE_SIZE)

    @property
    def buffer_size(self) -> int:
        """The number of non-padding bits in the color buffer."""
        return egl.eglGetConfigAttrib(self._display, self, egl.EGL_BUFFER_SIZE)

    @property
    def config_caveat(self) -> Optional[ConfigCaveat]:
        """Any caveat that applies when using this config."""
        caveat = ConfigCaveat(egl.eglGetConfigAttrib(self._display, self,
                                                     egl.EGL_CONFIG_CAVEAT))
        return None if caveat == ConfigCaveat.NONE else caveat

    @property
    def config_id(self) -> int:
        """The config's unique identifier."""
        return egl.eglGetConfigAttrib(self._display, self, egl.EGL_CONFIG_ID)

    @property
    def depth_size(self) -> int:
        """The number of bits in the depth buffer."""
        return egl.eglGetConfigAttrib(self._display, self, egl.EGL_DEPTH_SIZE)

    @property
    def green_size(self) -> int:
        """The number of color buffer bits used for green."""
        return egl.eglGetConfigAttrib(self._display, self, egl.EGL_GREEN_SIZE)

    @property
    def level(self) -> int:
        """The overlay or underlay level of the frame buffer."""
        return egl.eglGetConfigAttrib(self._display, self, egl.EGL_LEVEL)

    @property
    def max_pbuffer_height(self) -> int:
        """The maximum height in pixels of a pbuffer surface."""
        return egl.eglGetConfigAttrib(self._display, self,
                                      egl.EGL_MAX_PBUFFER_HEIGHT)

    @property
    def max_pbuffer_pixels(self) -> int:
        """The maximum number of pixels in a pbuffer surface."""
        return egl.eglGetConfigAttrib(self._display, self,
                                      egl.EGL_MAX_PBUFFER_PIXELS)

    @property
    def max_pbuffer_width(self) -> int:
        """The maximum width in pixels of a pbuffer surface."""
        return egl.eglGetConfigAttrib(self._display, self,
                                      egl.EGL_MAX_PBUFFER_WIDTH)

    @property
    def native_renderable(self) -> bool:
        """Whether native APIs can render to a surface."""
        return bool(egl.eglGetConfigAttrib(self._display, self,
                                           egl.EGL_NATIVE_RENDERABLE))

    @property
    def native_visual_id(self) -> int:
        """A platform-specific identifier for the native visual"""
        return egl.eglGetConfigAttrib(self._display, self,
                                       egl.EGL_NATIVE_VISUAL_ID)

    @property
    def native_visual_type(self) -> Any:
        """A platform-defined type for the native visual."""
        return egl.eglGetConfigAttrib(self._display, self,
                                       egl.EGL_NATIVE_VISUAL_TYPE)

    @property
    def red_size(self) -> int:
        """The number of color buffer bits used for red."""
        return egl.eglGetConfigAttrib(self._display, self, egl.EGL_RED_SIZE)

    @property
    def samples(self) -> int:
        """The number of samples per pixel."""
        return egl.eglGetConfigAttrib(self._display, self, egl.EGL_SAMPLES)

    @property
    def sample_buffers(self) -> int:
        """The number of multisample buffers."""
        return egl.eglGetConfigAttrib(self._display, self,
                                      egl.EGL_SAMPLE_BUFFERS)

    @property
    def stencil_size(self) -> int:
        """The number of bits in the stencil buffer."""
        return egl.eglGetConfigAttrib(self._display, self,
                                      egl.EGL_STENCIL_SIZE)

    @property
    def surface_type(self) -> SurfaceTypeFlag:
        """The type(s) of surface supported."""
        return SurfaceTypeFlag(egl.eglGetConfigAttrib(self._display, self,
                                                      egl.EGL_SURFACE_TYPE))

    @property
    def transparent_blue_value(self) -> int:
        """The blue value of the transparent color."""
        return egl.eglGetConfigAttrib(self._display, self,
                                      egl.EGL_TRANSPARENT_BLUE_VALUE)

    @property
    def transparent_green_value(self) -> int:
        """The green value of the transparent color."""
        return egl.eglGetConfigAttrib(self._display, self,
                                      egl.EGL_TRANSPARENT_GREEN_VALUE)

    @property
    def transparent_red_value(self) -> int:
        """The red value of the transparent color."""
        return egl.eglGetConfigAttrib(self._display, self,
                                      egl.EGL_TRANSPARENT_RED_VALUE)

    @property
    def transparent_type(self) -> Optional[TransparentType]:
        """The type of transparency supported."""
        ttype = TransparentType(egl.eglGetConfigAttrib(
                                    self._display, self,
                                    egl.EGL_TRANSPARENT_TYPE))
        return None if ttype == TransparentType.NONE else ttype


# These are defined here to avoid a circular dependency issue, where the config
# module depends on the context or surface module, and vice versa.
def config(self) -> Config:
    handle = self.config_id
    return Config._new_or_existing(handle, self._display, handle)
Context.config = property(config, doc='The config object used to create this '
                          'context.')
Surface.config = property(config, doc='The config object used to create this '
                          'surface.')

if egl.egl_version >= (1, 1):
    @property
    def bind_to_texture_rgb(self) -> bool:
        """Whether or not RGB textures can be bound."""
        return bool(egl.eglGetConfigAttrib(self._display, self,
                                           egl.EGL_BIND_TO_TEXTURE_RGB))
    Config.bind_to_texture_rgb = bind_to_texture_rgb

    @property
    def bind_to_texture_rgba(self) -> bool:
        """Whether or not RGBA textures can be bound."""
        return bool(egl.eglGetConfigAttrib(self._display, self,
                                           egl.EGL_BIND_TO_TEXTURE_RGBA))
    Config.bind_to_texture_rgba = bind_to_texture_rgba

    def max_swap_interval(self) -> bool:
        """The maximum number of video frames between buffer swaps."""
        return bool(egl.eglGetConfigAttrib(self._display, self,
                                           egl.EGL_MAX_SWAP_INTERVAL))
    Config.max_swap_interval = property(max_swap_interval)

    def min_swap_interval(self) -> bool:
        """The minimum number of video frames between buffer swaps."""
        return bool(egl.eglGetConfigAttrib(self._display, self,
                                           egl.EGL_MIN_SWAP_INTERVAL))
    Config.min_swap_interval = property(min_swap_interval)


if egl.egl_version >= (1, 2):
    from .enums import ClientAPIFlag, ClientBufferType, ColorBufferType

    def create_pbuffer_from_client_buffer(
        self, buftype: ClientBufferType, buffer: Any,
        attribs: Optional[dict[SurfaceAttrib, Any]]=None) -> Surface:
        """Create a pbuffer (off-screen) surface from a client buffer."""
        return Surface(self._display,
                       egl.eglCreatePbufferFromClientBuffer(
                           self._display, buftype, buffer, self,
                           attrib_list(attribs)))
    Config.create_pbuffer_from_client_buffer = \
        create_pbuffer_from_client_buffer

    def alpha_mask_size(self) -> int:
        """The number of bits in the alpha mask buffer."""
        return egl.eglGetConfigAttrib(self._display, self,
                                      egl.EGL_ALPHA_MASK_SIZE)
    Config.alpha_mask_size = property(alpha_mask_size)

    def color_buffer_type(self) -> ColorBufferType:
        """The type of color buffer."""
        return ColorBufferType(egl.eglGetConfigAttrib(
                                   self._display, self,
                                   egl.EGL_COLOR_BUFFER_TYPE))
    Config.color_buffer_type = property(color_buffer_type)

    def luminance_size(self) -> int:
        """The number of color buffer bits used for luminance."""
        return egl.eglGetConfigAttrib(self._display, self,
                                      egl.EGL_LUMINANCE_SIZE)
    Config.luminance_size = property(luminance_size)

    def renderable_type(self) -> ClientAPIFlag:
        """The supported client API(s)."""
        return ClientAPIFlag(egl.eglGetConfigAttrib(self._display, self,
                                                    egl.EGL_RENDERABLE_TYPE))
    Config.renderable_type = property(renderable_type)


if egl.egl_version >= (1, 3):
    # ClientAPIFlag already imported under version 1.2, above.
    @property
    def conformant(self) -> ClientAPIFlag:
        """Client APIs for which conformance requirements are met."""
        return ClientAPIFlag(egl.eglGetConfigAttrib(self._display, self,
                                                    egl.EGL_CONFORMANT))
    Config.conformant = conformant


if egl.egl_version >= (1, 5):
    def create_platform_pixmap_surface(self, native_pixmap: int,
                                       attribs: Optional[dict[SurfaceAttrib,
                                                              Any]]=None
                                       ) -> Surface:
        """Create a pixmap (off-screen) rendering surface."""
        return Surface(self._display,
                       egl.eglCreatePlatformPixmapSurface(
                           self._display, self, native_pixmap,
                           attrib_list(attribs, new_type=True)))
    Config.create_platform_pixmap_surface = create_platform_pixmap_surface

    def create_platform_window_surface(self, native_window: int,
                                       attribs: Optional[dict[SurfaceAttrib,
                                                              Any]]=None
                                       ) -> Surface:
        """Create a window (on-screen) rendering surface."""
        return Surface(self._display,
                       egl.eglCreatePlatformWindowSurface(
                           self._display, self, native_window,
                           attrib_list(attribs, new_type=True)))
    Config.create_platform_window_surface = create_platform_window_surface
