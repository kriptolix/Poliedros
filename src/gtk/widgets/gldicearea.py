# gldicearea.py
#
# Copyright 2024 k
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from gi.repository import Gtk

import numpy as np

from pydice3d.renderer import Renderer
from pydice3d.simulation import DiceSimulation
from OpenGL import GL


class GLDiceArea(Gtk.GLArea):

    def __init__(self) -> None:
        super().__init__()

        self.set_required_version(3, 3)
        self.set_has_depth_buffer(True)
        self.set_focusable(False)

        # Framebuffer dimensions in physical pixels.
        # DO NOT use get_allocated_width/height in _on_render: in HiDPI they
        # return logical pixels and the viewport would only cover 1/4 of the area.
        self._vp_w: int = 660
        self._vp_h: int = 460

        self._sim = DiceSimulation()

        self._renderer:  Renderer | None = None
        self._atlas_json: dict | None = None

        self.connect("realize",   self._on_realize)
        self.connect("unrealize", self._on_unrealize)
        self.connect("render",    self._on_render)
        self.connect("resize",    self._on_resize)

        ### a little zoom on dice
        eye = self._sim._camera.eye_position()
        target = np.asarray(self._sim._camera.target, float)

        direction = eye - target
        new_eye = target + direction / 1.5

        self._sim.set_camera(eye=new_eye)

    @property
    def simulation(self) -> DiceSimulation:
        return self._sim

    @property
    def simulating(self) -> bool:
        return self._sim.is_rolling

    @property
    def theme(self) -> str:
        return self._sim.theme

    @theme.setter
    def theme(self, value: str) -> None:
        self._sim.theme = value
        if self._renderer:
            self._renderer.theme = value
        self.queue_render()    

    def _on_resize(self, _area, width: int, height: int) -> None:
        self._vp_w = max(width, 1)
        self._vp_h = max(height, 1)
        self._sim.resize(self._vp_w, self._vp_h)

    def _on_realize(self, _area) -> None:
        self.make_current()
        if self.get_error():
            return

    def _on_unrealize(self, _area) -> None:
        self.make_current()
        if self._renderer:
            self._renderer.delete()
            self._renderer = None

    def _on_render(self, _area, _ctx) -> bool:
        w, h = self._vp_w, self._vp_h

        self._sim.step()
        scene = self._sim.scene

        if self._renderer and scene:
            VP = self._sim.view_projection()
            cam_pos = self._sim.camera_position()
            self._renderer.draw(scene, VP, cam_pos, w, h)

        else:
            GL.glViewport(0, 0, w, h)
            GL.glClearColor(0.0, 0.0, 0.0, 0.0)
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        return True

    def start_simulation(
        self,
        audio: bool,
        spec:    dict[str, int],
        targets: dict[str, list[int]] | None = None,
    ) -> None:
        """
        Record and start playback of a roll.    
        """
        self.make_current()
        if self.get_error():
            return

        self._sim.audio_enabled = audio       
        self._sim.roll(spec, theme=self._sim.theme, targets=targets)

        if self._renderer is None:
            self._renderer = Renderer(
                self._sim.scene,
                self._sim.dice_types,
                theme=self._sim.theme,
            )
        else:
            self._renderer.reload(self._sim.scene, self._sim.dice_types)
        
        # Must happen after Renderer is built/reloaded (dice_gpu must exist).        
        self._sim.apply_glyph_remaps(self._renderer)
        

       

    
