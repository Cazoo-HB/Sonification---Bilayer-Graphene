
"""
Created on Tue Feb 24 15:48:58 2026

@author: cedriccazorla
"""

import sys
import numpy as np
from pythonosc.udp_client import SimpleUDPClient

try:
    from PyQt5 import QtWidgets, QtCore, QtGui
    from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                                   QHBoxLayout, QLabel, QGroupBox, QGridLayout, 
                                   QDoubleSpinBox, QSpinBox, QPushButton, QFileDialog, QCheckBox)
except ImportError:
    print("Erreur : PyQt5 manquant. Installez-le via 'pip install PyQt5'")
    sys.exit(1)

import pyqtgraph as pg

class MoireProbeStation(QMainWindow):
    def __init__(self):
        super().__init__()
        self.lib_data = None
        self.osc_client = None
        self._block_signals = False # Verrou pour éviter les crashs
        
        self.initUI()
        self.setup_osc()
        
    def initUI(self):
        self.setWindowTitle("Moire Probe Station")
        self.setGeometry(100, 100, 1400, 950)
        pg.setConfigOption('background', 'k')
        pg.setConfigOption('foreground', 'w')
        
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        
        # --- PANNEAU CONTROLES ---
        controls = QWidget(); controls.setFixedWidth(360)
        clayout = QVBoxLayout(controls)
        
        # 1. Bibliothèque
        lib_group = QGroupBox("1. Data Library")
        l_lay = QVBoxLayout(); btn_load = QPushButton("Load Library (.npz)")
        btn_load.clicked.connect(self.load_library)
        self.lbl_info = QLabel("No data loaded")
        l_lay.addWidget(btn_load); l_lay.addWidget(self.lbl_info)
        lib_group.setLayout(l_lay); clayout.addWidget(lib_group)

        # 2. Coordonnées de la Sonde
        pr_group = QGroupBox("2. Free Probe Control")
        pr_lay = QGridLayout()
        self.sp_x1 = self.create_k_spin(); self.sp_y1 = self.create_k_spin()
        self.sp_x2 = self.create_k_spin(); self.sp_y2 = self.create_k_spin()
        self.lbl_p1 = QLabel("P1: r=0, θ=0"); self.lbl_p2 = QLabel("P2: r=0, θ=0")
        self.lbl_p1.setStyleSheet("color: #00FFFF;"); self.lbl_p2.setStyleSheet("color: #00FFFF;")
        
        pr_lay.addWidget(QLabel("P1 Kx:"), 0, 0); pr_lay.addWidget(self.sp_x1, 0, 1)
        pr_lay.addWidget(QLabel("P1 Ky:"), 1, 0); pr_lay.addWidget(self.sp_y1, 1, 1)
        pr_lay.addWidget(QLabel("P2 Kx:"), 2, 0); pr_lay.addWidget(self.sp_x2, 2, 1)
        pr_lay.addWidget(QLabel("P2 Ky:"), 3, 0); pr_lay.addWidget(self.sp_y2, 3, 1)
        pr_lay.addWidget(self.lbl_p1, 4, 0, 1, 2); pr_lay.addWidget(self.lbl_p2, 5, 0, 1, 2)
        pr_group.setLayout(pr_lay); clayout.addWidget(pr_group)

        # 3. Navigation
        nav_group = QGroupBox("3. Physics & View")
        n_lay = QGridLayout()
        self.spin_alpha = QDoubleSpinBox(); self.spin_alpha.setDecimals(3); self.spin_alpha.setSingleStep(0.001)
        self.spin_zoom = QDoubleSpinBox(); self.spin_zoom.setRange(1, 300); self.spin_zoom.setValue(50)
        self.sp_width = QSpinBox(); self.sp_width.setRange(1, 50); self.sp_width.setValue(3)
        
        btn_apply_zoom = QPushButton("Reset View to Zoom Scale")
        btn_apply_zoom.clicked.connect(self.apply_zoom_fixed)

        n_lay.addWidget(QLabel("Alpha α (°):"), 0, 0); n_lay.addWidget(self.spin_alpha, 0, 1)
        n_lay.addWidget(QLabel("Zoom Scale:"), 1, 0); n_lay.addWidget(self.spin_zoom, 1, 1)
        n_lay.addWidget(QLabel("Probe Width:"), 2, 0); n_lay.addWidget(self.sp_width, 2, 1)
        n_lay.addWidget(btn_apply_zoom, 3, 0, 1, 2)
        nav_group.setLayout(n_lay); clayout.addWidget(nav_group)

        # 4. OSC Control
        osc_group = QGroupBox("4. OSC Dual Stream")
        o_lay = QGridLayout()
        self.sp_nbins = QSpinBox(); self.sp_nbins.setRange(10, 2048); self.sp_nbins.setValue(400)
        self.txt_ip = QtWidgets.QLineEdit("127.0.0.1")
        self.sp_port = QSpinBox(); self.sp_port.setRange(1000, 9999); self.sp_port.setValue(9000)
        self.chk_osc = QCheckBox("Live Streaming"); self.chk_osc.setChecked(True)
        
        o_lay.addWidget(QLabel("Partials (N):"), 0, 0); o_lay.addWidget(self.sp_nbins, 0, 1)
        o_lay.addWidget(QLabel("IP:"), 1, 0); o_lay.addWidget(self.txt_ip, 1, 1)
        o_lay.addWidget(QLabel("Port:"), 2, 0); o_lay.addWidget(self.sp_port, 2, 1)
        o_lay.addWidget(self.chk_osc, 3, 0, 1, 2)
        btn_osc = QPushButton("Apply Connection"); btn_osc.clicked.connect(self.setup_osc)
        o_lay.addWidget(btn_osc, 4, 0, 1, 2)
        osc_group.setLayout(o_lay); clayout.addWidget(osc_group)

        # 5. Mapping
        dyn_group = QGroupBox("5. Dynamic Mapping")
        d_lay = QGridLayout()
        self.sp_vmin = QDoubleSpinBox(); self.sp_vmin.setRange(-5, 20); self.sp_vmin.setValue(3.5)
        self.sp_vmax = QDoubleSpinBox(); self.sp_vmax.setRange(-5, 20); self.sp_vmax.setValue(8.5)
        d_lay.addWidget(QLabel("Vmin:"), 0, 0); d_lay.addWidget(self.sp_vmin, 0, 1)
        d_lay.addWidget(QLabel("Vmax:"), 1, 0); d_lay.addWidget(self.sp_vmax, 1, 1)
        dyn_group.setLayout(d_lay); clayout.addWidget(dyn_group)

        # Connexions
        for s in [self.sp_x1, self.sp_y1, self.sp_x2, self.sp_y2]:
            s.valueChanged.connect(self.update_roi_from_spins)
        for w in [self.spin_alpha, self.sp_nbins, self.sp_vmin, self.sp_vmax, self.sp_width]:
            w.valueChanged.connect(self.update_view)
        self.spin_zoom.valueChanged.connect(self.apply_zoom_fixed)

        clayout.addStretch(); main_layout.addWidget(controls)

        # --- PANNEAU DROIT : AFFICHAGE ALPHA + GRAPHIQUE ---
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        # Le grand lecteur Alpha
        self.lbl_big_alpha = QLabel("Alpha α = -- °")
        self.lbl_big_alpha.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_big_alpha.setStyleSheet("font-size: 40px; font-weight: bold; color: #00FFFF; background-color: #111111; border-radius: 8px; padding: 10px; margin-bottom: 10px;")
        right_layout.addWidget(self.lbl_big_alpha)

        plot_area = pg.GraphicsLayoutWidget()
        right_layout.addWidget(plot_area, stretch=1)
        main_layout.addWidget(right_panel, stretch=1)
        
        self.p_img = plot_area.addPlot(row=0, col=0, title="FFT MONITOR (WYSIWYG)")
        self.p_img.setAspectLocked(True)
        # EMPECHE LE ZOOM DE REPARTIR A ZERO
        self.p_img.getViewBox().disableAutoRange() 
        
        self.img = pg.ImageItem(); self.p_img.addItem(self.img)
        
        # Segment ajustable
        self.roi = pg.LineSegmentROI([[0, 0], [10, 10]], pen=pg.mkPen('#00FFFF', width=3))
        self.p_img.addItem(self.roi)
        self.roi.sigRegionChanged.connect(self.update_spins_from_roi)
        
        # NOTE : Le graphique p_cut (Intensité & Rayon) a été supprimé ici !

    # --- LOGIQUE ---

    def create_k_spin(self):
        s = QDoubleSpinBox(); s.setRange(-300, 300); s.setSingleStep(0.1); s.setDecimals(2); return s

    def setup_osc(self):
        self.osc_client = SimpleUDPClient(self.txt_ip.text(), self.sp_port.value())

    def apply_zoom_fixed(self):
        """Force le zoom à la valeur du spinbox uniquement quand on le demande."""
        z = self.spin_zoom.value()
        self.p_img.setXRange(-z, z, padding=0)
        self.p_img.setYRange(-z, z, padding=0)

    def load_library(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open Lib", "", "*.npz")
        if path:
            d = np.load(path); self.lib_data = {k: d[k] for k in d.files}
            self.spin_alpha.setRange(self.lib_data['angles'][0], self.lib_data['angles'][-1])
            self.lbl_info.setText(f"Loaded: {len(self.lib_data['angles'])} frames")
            self.apply_zoom_fixed() # Zoom initial
            self.update_view()

    def update_spins_from_roi(self):
        if self._block_signals: return
        self._block_signals = True
        st = self.roi.getState(); pos, pts = st['pos'], st['points']
        p1 = [pos.x() + pts[0].x(), pos.y() + pts[0].y()]
        p2 = [pos.x() + pts[1].x(), pos.y() + pts[1].y()]
        self.sp_x1.setValue(p1[0]); self.sp_y1.setValue(p1[1])
        self.sp_x2.setValue(p2[0]); self.sp_y2.setValue(p2[1])
        self.update_polar(p1, p2)
        self._block_signals = False
        self.update_view()

    def update_roi_from_spins(self):
        if self._block_signals: return
        self._block_signals = True
        p1 = [self.sp_x1.value(), self.sp_y1.value()]
        p2 = [self.sp_x2.value(), self.sp_y2.value()]
        state = {'pos': QtCore.QPointF(p1[0], p1[1]), 'points': [QtCore.QPointF(0, 0), QtCore.QPointF(p2[0]-p1[0], p2[1]-p1[1])]}
        self.roi.setState(state)
        self.update_polar(p1, p2)
        self._block_signals = False
        self.update_view()

    def update_polar(self, p1, p2):
        r1, t1 = np.hypot(*p1), np.degrees(np.arctan2(p1[1], p1[0]))
        r2, t2 = np.hypot(*p2), np.degrees(np.arctan2(p2[1], p2[0]))
        self.lbl_p1.setText(f"P1: r={r1:.2f}, θ={t1:.1f}°"); self.lbl_p2.setText(f"P2: r={r2:.2f}, θ={t2:.1f}°")

    def update_view(self):
        if self.lib_data is None: return
        idx = np.argmin(np.abs(self.lib_data['angles'] - self.spin_alpha.value()))
        amp = self.lib_data['amplitudes'][idx]; kv = self.lib_data['k_vec']
        vmin, vmax = self.sp_vmin.value(), self.sp_vmax.value()
        
        # --- Mise à jour du grand lecteur Alpha ---
        actual_alpha = self.lib_data['angles'][idx]
        self.lbl_big_alpha.setText(f"Alpha α = {actual_alpha:.3f}°")
        
        # WYSIWYG : Traitement identique à l'écran
        visual_data = np.log1p(amp)
        # ON NE REINITIALISE PAS LE ZOOM ICI
        self.img.setImage(visual_data.T, levels=(vmin, vmax), autoRange=False)
        self.img.setRect(QtCore.QRectF(kv[0], kv[0], kv[-1]-kv[0], kv[-1]-kv[0]))
        
        try:
            # EXTRACTION DEPUIS LA VUE TRANSPOSEE (.T)
            sl = self.roi.getArrayRegion(visual_data.T, self.img)
            if sl is not None and len(sl) > 0:
                if sl.ndim > 1: sl = np.max(sl, axis=1) # Peak Detection
                
                # Normalisation intensité
                norm_int = np.clip((sl - vmin) / (vmax - vmin), 0, 1)
                
                # Coordonnées réelles pour les rayons
                p1, p2 = [self.sp_x1.value(), self.sp_y1.value()], [self.sp_x2.value(), self.sp_y2.value()]
                x_pts = np.linspace(p1[0], p2[0], len(norm_int))
                y_pts = np.linspace(p1[1], p2[1], len(norm_int))
                radius_list = np.sqrt(x_pts**2 + y_pts**2)
                
                # Resampling OSC
                nb = self.sp_nbins.value()
                final_int = np.interp(np.linspace(0, 1, nb), np.linspace(0, 1, len(norm_int)), norm_int)
                final_rad = np.interp(np.linspace(0, 1, nb), np.linspace(0, 1, len(radius_list)), radius_list)
                
                # NOTE : Les mises à jour graphiques (curve_int / curve_rad) ont été supprimées
                
                if self.chk_osc.isChecked() and self.osc_client: 
                    self.osc_client.send_message("/moire/intensity", final_int.tolist())
                    self.osc_client.send_message("/moire/radius", final_rad.tolist())
        except Exception as e: pass

if __name__ == '__main__':
    app = QApplication(sys.argv); app.setStyle('Fusion')
    win = MoireProbeStation(); win.show(); sys.exit(app.exec_())