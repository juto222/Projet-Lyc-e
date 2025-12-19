from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QSlider, QFrame,
                             QComboBox, QCheckBox, QGroupBox)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from OpenGL.GL import *
from OpenGL.GLU import *
import sys
import math
import numpy as np

class Advanced3DWidget(QOpenGLWidget):
    """Widget 3D ultra-avancé avec multiples objets et effets"""
    def __init__(self):
        super().__init__()
        self.camera_x = 0
        self.camera_y = 2
        self.camera_z = 15
        self.camera_angle_x = 0
        self.camera_angle_y = 0
        self.rotation = 0
        self.planet_rotation = 0
        self.auto_rotate = True
        self.show_wireframe = False
        self.show_grid = True
        self.show_axes = True
        self.lighting_enabled = True
        self.fog_enabled = False
        self.current_scene = "solar_system"
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_scene)
        self.timer.start(16)
        self.last_mouse_pos = None
        self.mouse_sensitivity = 0.3
        self.setMinimumSize(800, 600)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
    
    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)
        glShadeModel(GL_SMOOTH)
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_POSITION, [0, 0, 0, 1])
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.3, 0.3, 0.3, 1])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 0.9, 1])
        glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1])
        glEnable(GL_LIGHT1)
        glLightfv(GL_LIGHT1, GL_POSITION, [10, 5, 10, 1])
        glLightfv(GL_LIGHT1, GL_AMBIENT, [0.0, 0.0, 0.1, 1])
        glLightfv(GL_LIGHT1, GL_DIFFUSE, [0.3, 0.4, 0.8, 1])
        glLightfv(GL_LIGHT1, GL_SPECULAR, [0.5, 0.5, 1.0, 1])
        glEnable(GL_LIGHT2)
        glLightfv(GL_LIGHT2, GL_POSITION, [-10, -5, 5, 1])
        glLightfv(GL_LIGHT2, GL_AMBIENT, [0.1, 0.0, 0.1, 1])
        glLightfv(GL_LIGHT2, GL_DIFFUSE, [0.8, 0.2, 0.5, 1])
        glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
        glMaterialfv(GL_FRONT, GL_SHININESS, [50.0])
        glEnable(GL_LINE_SMOOTH)
        glEnable(GL_POLYGON_SMOOTH)
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)
        glClearColor(0.02, 0.02, 0.08, 1.0)
    
    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, w / h if h != 0 else 1, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
    
    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(-self.camera_x, -self.camera_y, -self.camera_z)
        glRotatef(self.camera_angle_x, 1, 0, 0)
        glRotatef(self.camera_angle_y, 0, 1, 0)
        if self.fog_enabled:
            glEnable(GL_FOG)
            glFogi(GL_FOG_MODE, GL_LINEAR)
            glFogfv(GL_FOG_COLOR, [0.02, 0.02, 0.08, 1.0])
            glFogf(GL_FOG_DENSITY, 0.05)
            glFogf(GL_FOG_START, 10.0)
            glFogf(GL_FOG_END, 30.0)
        else:
            glDisable(GL_FOG)
        if self.show_grid:
            self.draw_grid()
        if self.show_axes:
            self.draw_axes()
        if self.current_scene == "solar_system":
            self.draw_solar_system()
        elif self.current_scene == "geometric":
            self.draw_geometric_scene()
        elif self.current_scene == "crystal":
            self.draw_crystal_scene()
        elif self.current_scene == "city":
            self.draw_futuristic_city()
    
    def draw_grid(self):
        glDisable(GL_LIGHTING)
        glColor3f(0.2, 0.3, 0.5)
        glLineWidth(1)
        size = 20
        step = 1
        glBegin(GL_LINES)
        for i in range(-size, size + 1, step):
            glVertex3f(-size, 0, i)
            glVertex3f(size, 0, i)
            glVertex3f(i, 0, -size)
            glVertex3f(i, 0, size)
        glEnd()
        if self.lighting_enabled:
            glEnable(GL_LIGHTING)
    
    def draw_axes(self):
        glDisable(GL_LIGHTING)
        glLineWidth(3)
        glBegin(GL_LINES)
        glColor3f(1, 0, 0)
        glVertex3f(0, 0, 0)
        glVertex3f(3, 0, 0)
        glColor3f(0, 1, 0)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 3, 0)
        glColor3f(0, 0, 1)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 0, 3)
        glEnd()
        if self.lighting_enabled:
            glEnable(GL_LIGHTING)
    
    def draw_solar_system(self):
        glPushMatrix()
        glColor3f(1.0, 0.9, 0.2)
        glMaterialfv(GL_FRONT, GL_EMISSION, [0.8, 0.8, 0.0, 1.0])
        self.draw_sphere(1.5, 30, 30)
        glMaterialfv(GL_FRONT, GL_EMISSION, [0.0, 0.0, 0.0, 1.0])
        glPopMatrix()
        glPushMatrix()
        glRotatef(self.planet_rotation * 4, 0, 1, 0)
        glTranslatef(3, 0, 0)
        glColor3f(0.6, 0.6, 0.6)
        self.draw_sphere(0.3, 20, 20)
        glPopMatrix()
        glPushMatrix()
        glRotatef(self.planet_rotation * 2.5, 0, 1, 0)
        glTranslatef(4.5, 0, 0)
        glColor3f(0.9, 0.6, 0.2)
        self.draw_sphere(0.5, 20, 20)
        glPopMatrix()
        glPushMatrix()
        glRotatef(self.planet_rotation * 2, 0, 1, 0)
        glTranslatef(6.5, 0, 0)
        glColor3f(0.2, 0.5, 0.9)
        self.draw_sphere(0.6, 25, 25)
        glRotatef(self.planet_rotation * 8, 0, 1, 0)
        glTranslatef(1.2, 0, 0)
        glColor3f(0.8, 0.8, 0.8)
        self.draw_sphere(0.15, 15, 15)
        glPopMatrix()
        glPushMatrix()
        glRotatef(self.planet_rotation * 1.5, 0, 1, 0)
        glTranslatef(8.5, 0, 0)
        glColor3f(0.9, 0.3, 0.2)
        self.draw_sphere(0.45, 20, 20)
        glPopMatrix()
        glPushMatrix()
        glRotatef(self.planet_rotation, 0, 1, 0)
        glTranslatef(11, 0, 0)
        glColor3f(0.8, 0.7, 0.5)
        self.draw_sphere(1.2, 30, 30)
        glPopMatrix()
        self.draw_orbit_rings()
    
    def draw_geometric_scene(self):
        glPushMatrix()
        glRotatef(self.rotation, 1, 1, 0)
        glColor3f(0.3, 0.6, 0.9)
        self.draw_torus(0.8, 0.3, 30, 30)
        glPopMatrix()
        for i in range(6):
            angle = self.rotation + i * 60
            glPushMatrix()
            glRotatef(angle, 0, 1, 0)
            glTranslatef(4, 0, 0)
            glRotatef(self.rotation * 2, 1, 1, 1)
            r = 0.5 + 0.5 * math.sin(angle * 0.1)
            g = 0.5 + 0.5 * math.sin(angle * 0.1 + 2)
            b = 0.5 + 0.5 * math.sin(angle * 0.1 + 4)
            glColor3f(r, g, b)
            self.draw_cube(0.5)
            glPopMatrix()
        for i in range(4):
            angle = self.rotation * 0.5 + i * 90
            glPushMatrix()
            glRotatef(angle, 0, 1, 0)
            glTranslatef(6, math.sin(self.rotation * 0.05 + i) * 2, 0)
            glRotatef(self.rotation, 0, 1, 0)
            glColor3f(0.9, 0.3, 0.5)
            self.draw_pyramid(0.8)
            glPopMatrix()
    
    def draw_crystal_scene(self):
        glPushMatrix()
        glRotatef(self.rotation * 0.3, 0, 1, 0)
        glColor4f(0.3, 0.8, 0.9, 0.7)
        self.draw_crystal(2, 4, 6)
        glPopMatrix()
        for i in range(8):
            angle = self.rotation + i * 45
            glPushMatrix()
            glRotatef(angle, 0, 1, 0)
            glTranslatef(5, math.sin(angle * 0.1) * 2, 0)
            glRotatef(angle * 2, 1, 1, 1)
            if i % 3 == 0:
                glColor4f(0.8, 0.3, 0.9, 0.8)
            elif i % 3 == 1:
                glColor4f(0.3, 0.9, 0.5, 0.8)
            else:
                glColor4f(0.9, 0.8, 0.3, 0.8)
            self.draw_crystal(0.5, 1.5, 5)
            glPopMatrix()
        self.draw_particles()
    
    def draw_futuristic_city(self):
        glPushMatrix()
        glTranslatef(0, -0.1, 0)
        glColor3f(0.1, 0.2, 0.3)
        glBegin(GL_QUADS)
        glVertex3f(-15, 0, -15)
        glVertex3f(15, 0, -15)
        glVertex3f(15, 0, 15)
        glVertex3f(-15, 0, 15)
        glEnd()
        glPopMatrix()
        buildings = [
            (-5, 0, -5, 0.8, 5, 0.3, 0.5, 0.9),
            (-2, 0, -6, 0.6, 7, 0.5, 0.3, 0.8),
            (1, 0, -4, 0.7, 4, 0.8, 0.4, 0.3),
            (4, 0, -5, 0.9, 6, 0.2, 0.6, 0.9),
            (-6, 0, 2, 0.7, 8, 0.6, 0.3, 0.9),
            (-2, 0, 3, 0.5, 3, 0.9, 0.5, 0.3),
            (2, 0, 4, 0.8, 9, 0.3, 0.8, 0.5),
            (6, 0, 2, 0.6, 5, 0.8, 0.3, 0.6),
        ]
        for bx, by, bz, size, height, r, g, b in buildings:
            glPushMatrix()
            glTranslatef(bx, height/2, bz)
            glColor3f(r, g, b)
            self.draw_building(size, height, size)
            if height > 6:
                glTranslatef(0, height/2 + 0.5, 0)
                glColor3f(1, 0.2, 0.2)
                self.draw_cylinder(0.05, 2, 10)
            glPopMatrix()
        self.draw_flying_vehicles()
    
    def draw_sphere(self, radius, slices, stacks):
        quad = gluNewQuadric()
        gluQuadricNormals(quad, GLU_SMOOTH)
        gluSphere(quad, radius, slices, stacks)
        gluDeleteQuadric(quad)
    
    def draw_cube(self, size):
        glBegin(GL_QUADS)
        s = size / 2
        faces = [
            ([s, s, s], [s, -s, s], [-s, -s, s], [-s, s, s], [0, 0, 1]),
            ([s, s, -s], [-s, s, -s], [-s, -s, -s], [s, -s, -s], [0, 0, -1]),
            ([s, s, s], [s, s, -s], [s, -s, -s], [s, -s, s], [1, 0, 0]),
            ([-s, s, s], [-s, -s, s], [-s, -s, -s], [-s, s, -s], [-1, 0, 0]),
            ([s, s, s], [-s, s, s], [-s, s, -s], [s, s, -s], [0, 1, 0]),
            ([s, -s, s], [s, -s, -s], [-s, -s, -s], [-s, -s, s], [0, -1, 0])
        ]
        for face in faces:
            glNormal3fv(face[4])
            for vertex in face[:4]:
                glVertex3fv(vertex)
        glEnd()
    
    def draw_torus(self, major_radius, minor_radius, major_segments, minor_segments):
        for i in range(major_segments):
            glBegin(GL_QUAD_STRIP)
            for j in range(minor_segments + 1):
                for k in range(2):
                    s = (i + k) % major_segments + 0.5
                    t = j % minor_segments
                    angle1 = 2 * math.pi * s / major_segments
                    angle2 = 2 * math.pi * t / minor_segments
                    x = (major_radius + minor_radius * math.cos(angle2)) * math.cos(angle1)
                    y = (major_radius + minor_radius * math.cos(angle2)) * math.sin(angle1)
                    z = minor_radius * math.sin(angle2)
                    nx = math.cos(angle2) * math.cos(angle1)
                    ny = math.cos(angle2) * math.sin(angle1)
                    nz = math.sin(angle2)
                    glNormal3f(nx, ny, nz)
                    glVertex3f(x, y, z)
            glEnd()
    
    def draw_pyramid(self, size):
        glBegin(GL_TRIANGLES)
        s = size / 2
        h = size * 1.5
        glNormal3f(0, -1, 0)
        glVertex3f(s, 0, s)
        glVertex3f(-s, 0, -s)
        glVertex3f(-s, 0, s)
        glVertex3f(s, 0, s)
        glVertex3f(s, 0, -s)
        glVertex3f(-s, 0, -s)
        glNormal3f(0, 0.7, 0.7)
        glVertex3f(0, h, 0)
        glVertex3f(-s, 0, s)
        glVertex3f(s, 0, s)
        glNormal3f(0.7, 0.7, 0)
        glVertex3f(0, h, 0)
        glVertex3f(s, 0, s)
        glVertex3f(s, 0, -s)
        glNormal3f(0, 0.7, -0.7)
        glVertex3f(0, h, 0)
        glVertex3f(s, 0, -s)
        glVertex3f(-s, 0, -s)
        glNormal3f(-0.7, 0.7, 0)
        glVertex3f(0, h, 0)
        glVertex3f(-s, 0, -s)
        glVertex3f(-s, 0, s)
        glEnd()
    
    def draw_crystal(self, base_radius, height, sides):
        glBegin(GL_TRIANGLES)
        angle_step = 2 * math.pi / sides
        for i in range(sides):
            angle1 = i * angle_step
            angle2 = (i + 1) * angle_step
            x1 = base_radius * math.cos(angle1)
            z1 = base_radius * math.sin(angle1)
            x2 = base_radius * math.cos(angle2)
            z2 = base_radius * math.sin(angle2)
            glVertex3f(0, height, 0)
            glVertex3f(x1, 0, z1)
            glVertex3f(x2, 0, z2)
        for i in range(sides):
            angle1 = i * angle_step
            angle2 = (i + 1) * angle_step
            x1 = base_radius * math.cos(angle1)
            z1 = base_radius * math.sin(angle1)
            x2 = base_radius * math.cos(angle2)
            z2 = base_radius * math.sin(angle2)
            glVertex3f(0, -height/2, 0)
            glVertex3f(x2, 0, z2)
            glVertex3f(x1, 0, z1)
        glEnd()
    
    def draw_building(self, width, height, depth):
        glPushMatrix()
        glScalef(width, height, depth)
        self.draw_cube(1)
        glPopMatrix()
        glDisable(GL_LIGHTING)
        window_color = [1.0, 0.9, 0.6]
        num_floors = int(height / 0.5)
        for floor in range(num_floors):
            y = -height/2 + floor * 0.5 + 0.2
            for x in np.linspace(-width/2 + 0.1, width/2 - 0.1, 3):
                if (floor + int(x * 10)) % 3 != 0:
                    glColor3fv(window_color)
                    glBegin(GL_QUADS)
                    glVertex3f(x, y, depth/2 + 0.01)
                    glVertex3f(x + 0.1, y, depth/2 + 0.01)
                    glVertex3f(x + 0.1, y + 0.3, depth/2 + 0.01)
                    glVertex3f(x, y + 0.3, depth/2 + 0.01)
                    glEnd()
        if self.lighting_enabled:
            glEnable(GL_LIGHTING)
    
    def draw_cylinder(self, radius, height, slices):
        quad = gluNewQuadric()
        gluCylinder(quad, radius, radius, height, slices, 1)
        gluDeleteQuadric(quad)
    
    def draw_orbit_rings(self):
        glDisable(GL_LIGHTING)
        glLineWidth(1)
        orbits = [3, 4.5, 6.5, 8.5, 11]
        for radius in orbits:
            glColor4f(0.3, 0.5, 0.8, 0.3)
            glBegin(GL_LINE_LOOP)
            for i in range(100):
                angle = 2 * math.pi * i / 100
                x = radius * math.cos(angle)
                z = radius * math.sin(angle)
                glVertex3f(x, 0, z)
            glEnd()
        if self.lighting_enabled:
            glEnable(GL_LIGHTING)
    
    def draw_particles(self):
        glDisable(GL_LIGHTING)
        glPointSize(3)
        glBegin(GL_POINTS)
        for i in range(50):
            angle = self.rotation * 0.5 + i * 7.2
            radius = 3 + (i % 5)
            height = math.sin(self.rotation * 0.1 + i) * 3
            x = radius * math.cos(math.radians(angle))
            z = radius * math.sin(math.radians(angle))
            glColor4f(0.8, 0.9, 1.0, 0.6)
            glVertex3f(x, height, z)
        glEnd()
        if self.lighting_enabled:
            glEnable(GL_LIGHTING)
    
    def draw_flying_vehicles(self):
        for i in range(4):
            angle = self.rotation * 2 + i * 90
            glPushMatrix()
            glRotatef(angle, 0, 1, 0)
            glTranslatef(8, 3 + math.sin(self.rotation * 0.1 + i) * 0.5, 0)
            glRotatef(90, 0, 1, 0)
            glColor3f(0.8, 0.2, 0.2)
            glScalef(0.3, 0.1, 0.15)
            self.draw_cube(1)
            glPopMatrix()
    
    def update_scene(self):
        if self.auto_rotate:
            self.rotation += 1
            self.planet_rotation += 0.5
        self.update()
    
    def mousePressEvent(self, event):
        self.last_mouse_pos = event.pos()
    
    def mouseMoveEvent(self, event):
        if self.last_mouse_pos and event.buttons() & Qt.MouseButton.LeftButton:
            dx = event.pos().x() - self.last_mouse_pos.x()
            dy = event.pos().y() - self.last_mouse_pos.y()
            self.camera_angle_y += dx * self.mouse_sensitivity
            self.camera_angle_x += dy * self.mouse_sensitivity
            self.camera_angle_x = max(-89, min(89, self.camera_angle_x))
            self.last_mouse_pos = event.pos()
    
    def mouseReleaseEvent(self, event):
        self.last_mouse_pos = None
    
    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        self.camera_z -= delta / 120.0
        self.camera_z = max(5, min(50, self.camera_z))
    
    def keyPressEvent(self, event):
        speed = 0.5
        if event.key() == Qt.Key.Key_W:
            self.camera_z -= speed
        elif event.key() == Qt.Key.Key_S:
            self.camera_z += speed
        elif event.key() == Qt.Key.Key_A:
            self.camera_x -= speed
        elif event.key() == Qt.Key.Key_D:
            self.camera_x += speed
        elif event.key() == Qt.Key.Key_Q:
            self.camera_y += speed
        elif event.key() == Qt.Key.Key_E:
            self.camera_y -= speed


class Ultimate3DWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🌌 Visualisation 3D Ultra-Avancée")
        self.setGeometry(100, 100, 1400, 900)
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #0a0e27, stop:1 #1a1f3a);
            }
        """)
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        self.gl_widget = Advanced3DWidget()
        control_panel = self.create_control_panel()
        main_layout.addWidget(self.gl_widget, stretch=3)
        main_layout.addWidget(control_panel, stretch=1)
        central.setLayout(main_layout)
    
    def create_control_panel(self):
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background: rgba(20, 30, 60, 0.8);
                border: 2px solid rgba(96, 165, 250, 0.3);
                border-radius: 15px;
                padding: 15px;
            }
            QLabel {
                color: white;
                font-weight: bold;
            }
            QPushButton {
                background: #3b82f6;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #2563eb;
            }
            QComboBox {
                background: #1e3a8a;
                color: white;
                border: 1px solid #3b82f6;
                border-radius: 5px;
                padding: 5px;
            }
            QCheckBox {
                color: white;
            }
        """)
        layout = QVBoxLayout()
        layout.setSpacing(15)
        title = QLabel("🎮 CONTRÔLES 3D")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #60a5fa;")
        layout.addWidget(title)
        scene_group = QGroupBox("🌍 Scène")
        scene_group.setStyleSheet("QGroupBox { color: white; font-weight: bold; }")
        scene_layout = QVBoxLayout()
        self.scene_combo = QComboBox()
        self.scene_combo.addItems([
            "Système Solaire",
            "Formes Géométriques", 
            "Cristaux",
            "Ville Futuriste"
        ])
        self.scene_combo.currentIndexChanged.connect(self.change_scene)
        scene_layout.addWidget(self.scene_combo)
        scene_group.setLayout(scene_layout)
        layout.addWidget(scene_group)
        anim_group = QGroupBox("⚡ Animation")
        anim_group.setStyleSheet("QGroupBox { color: white; font-weight: bold; }")
        anim_layout = QVBoxLayout()
        pause_btn = QPushButton("⏸️ Pause/Play")
        pause_btn.clicked.connect(self.toggle_animation)
        anim_layout.addWidget(pause_btn)
        reset_btn = QPushButton("🔄 Réinitialiser")
        reset_btn.clicked.connect(self.reset_camera)
        anim_layout.addWidget(reset_btn)
        anim_group.setLayout(anim_layout)
        layout.addWidget(anim_group)
        display_group = QGroupBox("👁️ Affichage")
        display_group.setStyleSheet("QGroupBox { color: white; font-weight: bold; }")
        display_layout = QVBoxLayout()
        self.wireframe_check = QCheckBox("Mode Wireframe")
        self.wireframe_check.stateChanged.connect(self.toggle_wireframe)
        display_layout.addWidget(self.wireframe_check)
        self.grid_check = QCheckBox("Grille")
        self.grid_check.setChecked(True)
        self.grid_check.stateChanged.connect(self.toggle_grid)
        display_layout.addWidget(self.grid_check)
        self.axes_check = QCheckBox("Axes XYZ")
        self.axes_check.setChecked(True)
        self.axes_check.stateChanged.connect(self.toggle_axes)
        display_layout.addWidget(self.axes_check)
        self.lighting_check = QCheckBox("Éclairage")
        self.lighting_check.setChecked(True)
        self.lighting_check.stateChanged.connect(self.toggle_lighting)
        display_layout.addWidget(self.lighting_check)
        self.fog_check = QCheckBox("Brouillard")
        self.fog_check.stateChanged.connect(self.toggle_fog)
        display_layout.addWidget(self.fog_check)
        display_group.setLayout(display_layout)
        layout.addWidget(display_group)
        info_group = QGroupBox("ℹ️ Contrôles")
        info_group.setStyleSheet("QGroupBox { color: white; font-weight: bold; }")
        info_layout = QVBoxLayout()
        info_text = QLabel(
            "🖱️ Clic gauche + Déplacer: Rotation\n"
            "🖱️ Molette: Zoom\n"
            "⌨️ W/S: Avant/Arrière\n"
            "⌨️ A/D: Gauche/Droite\n"
            "⌨️ Q/E: Haut/Bas"
        )
        info_text.setStyleSheet("color: rgba(255, 255, 255, 0.8); font-size: 10px;")
        info_text.setWordWrap(True)
        info_layout.addWidget(info_text)
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        layout.addStretch()
        panel.setLayout(layout)
        return panel
    
    def change_scene(self, index):
        scenes = ["solar_system", "geometric", "crystal", "city"]
        self.gl_widget.current_scene = scenes[index]
    
    def toggle_animation(self):
        self.gl_widget.auto_rotate = not self.gl_widget.auto_rotate
    
    def reset_camera(self):
        self.gl_widget.camera_x = 0
        self.gl_widget.camera_y = 2
        self.gl_widget.camera_z = 15
        self.gl_widget.camera_angle_x = 0
        self.gl_widget.camera_angle_y = 0
        self.gl_widget.rotation = 0
        self.gl_widget.planet_rotation = 0
    
    def toggle_wireframe(self, state):
        self.gl_widget.show_wireframe = bool(state)
        if state:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    
    def toggle_grid(self, state):
        self.gl_widget.show_grid = bool(state)
    
    def toggle_axes(self, state):
        self.gl_widget.show_axes = bool(state)
    
    def toggle_lighting(self, state):
        self.gl_widget.lighting_enabled = bool(state)
    
    def toggle_fog(self, state):
        self.gl_widget.fog_enabled = bool(state)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = Ultimate3DWindow()
    window.show()
    sys.exit(app.exec())

# Installation: pip install PyQt6 PyOpenGL PyOpenGL_accelerate numpy