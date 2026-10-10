# Implementation Plan

## Project
**Real-Time Document Scanner and Chromatic Verification Mark Extractor Using Planar Homography and Adaptive Image Segmentation**

- **Status:** Not started
- **Estimated duration:** 4–6 weeks at ~1–2 hours/day (adjust to experience and testing needs)
- **Approach:** Build a testable OpenCV MVP before adding a richer GUI.
- **Stack:** Python 3.11/3.12, OpenCV, NumPy; optional PySide6 and Pillow.

## 1. Definition of done
The application must capture webcam frames, detect a valid four-corner document, correct perspective, generate a high-contrast scan, create blue/red ink masks and extracted candidate images, display diagnostic views, and export matching artifacts. All stages must handle missing/invalid inputs. Benchmark actual FPS and latency; 30+ FPS is a target, not a guaranteed outcome.

## 2. Proposed repository structure
```text
document-scanner-cv/
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
├── src/
│   ├── __init__.py
│   ├── camera.py
│   ├── preprocessing.py
│   ├── document_detector.py
│   ├── perspective.py
│   ├── enhancement.py
│   ├── color_extractor.py
│   ├── pipeline.py
│   ├── dashboard.py
│   └── exporter.py
├── tests/
│   ├── test_detector.py
│   ├── test_perspective.py
│   ├── test_enhancement.py
│   └── test_color_extractor.py
├── samples/
└── output/
```
Implement modules incrementally. Exclude generated outputs and local virtual environments from Git.

## 3. Phase-by-phase task plan

### Phase 1 — Setup and live camera (Week 1)
**Objective:** Reliable webcam capture.

- [ ] **1.1** Create repository and folders.
- [ ] **1.2** Create Python virtual environment and install OpenCV/NumPy.
- [ ] **1.3** Create `.gitignore` for `.venv/`, `__pycache__/`, and generated `output/`.
- [ ] **1.4** Implement `src/camera.py`: open webcam, read frames, handle failure, release resources.
- [ ] **1.5** Implement minimal `main.py` loop with `cv2.imshow` and `q` exit.
- [ ] **1.6** Record input resolution and baseline capture FPS.

**Commands (Windows PowerShell):**
```powershell
mkdir document-scanner-cv
cd document-scanner-cv
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install opencv-python numpy
pip freeze > requirements.txt
```
If PowerShell activation is restricted, use `.venv\Scripts\python.exe` directly.

**Acceptance:** Webcam feed displays; missing camera produces a useful message; `q` exits cleanly.

### Phase 2 — Preprocessing and boundary detection (Week 1)
**Objective:** Find the document's four corners.

- [ ] **2.1** Implement frame resizing and grayscale conversion in `src/preprocessing.py`.
- [ ] **2.2** Add Gaussian blur; benchmark optional bilateral filtering separately.
- [ ] **2.3** Generate Canny edge map; start with thresholds 50/150, tune using samples.
- [ ] **2.4** Use `cv2.findContours` and rank plausible candidates by area.
- [ ] **2.5** Use `cv2.approxPolyDP` with starting epsilon `0.02 * perimeter`.
- [ ] **2.6** Reject small, non-convex, degenerate, or implausible quadrilaterals.
- [ ] **2.7** Draw corners and outline on live feed.
- [ ] **2.8** Return `None` explicitly when no valid document is detected.
- [ ] **2.9** Test plain/cluttered backgrounds and different document angles.

**Acceptance:** Valid convex four-corner detection on representative fully visible pages; no crash when document disappears.

### Phase 3 — Perspective rectification (Week 2)
**Objective:** Generate upright rectangular document images.

- [ ] **3.1** Implement robust corner ordering: TL, TR, BR, BL.
- [ ] **3.2** Calculate output width/height from edge lengths; clamp unreasonable sizes.
- [ ] **3.3** Build destination rectangle coordinates.
- [ ] **3.4** Compute 3×3 homography using `cv2.getPerspectiveTransform`.
- [ ] **3.5** Warp with `cv2.warpPerspective` using original color frame.
- [ ] **3.6** Add tests for rotated corner input, degenerate polygons, and output geometry.
- [ ] **3.7** Compare rectified results at several viewing angles.

**Acceptance:** Correct orientation and readable perspective-corrected output for valid planar pages.

### Phase 4 — Enhancement and clean scan (Week 2)
**Objective:** Create usable digital scan variants.

- [ ] **4.1** Keep original rectified BGR image for color segmentation.
- [ ] **4.2** Convert rectified image to grayscale.
- [ ] **4.3** Implement `cv2.adaptiveThreshold` (Gaussian, binary; initial block size 21, C=10).
- [ ] **4.4** Tune block size and C against shadows and fine text.
- [ ] **4.5** Compare color, grayscale, and binary results side by side.
- [ ] **4.6** Test thin writing, paper creases, and uneven lighting.

**Acceptance:** Exportable readable scan with documented limitations for severe shadows/creases.

### Phase 5 — HSV ink/stamp extraction (Week 3)
**Objective:** Isolate blue/red color-selected marks.

- [ ] **5.1** Convert the rectified **color** document from BGR to HSV.
- [ ] **5.2** Define configurable blue HSV range (initial H=90–140, S>=50, V>=40).
- [ ] **5.3** Define two red hue ranges to handle hue wrap-around (tune against samples).
- [ ] **5.4** Create masks with `cv2.inRange`; merge red intervals with bitwise OR.
- [ ] **5.5** Tune opening/closing kernels; avoid erasing thin strokes.
- [ ] **5.6** Find connected components/contours and optionally reject tiny noise regions.
- [ ] **5.7** Create color-preserving isolated outputs and optional transparent PNGs.
- [ ] **5.8** Preserve raw and cleaned masks for debugging.
- [ ] **5.9** Test blue ink, red stamps, both, none, and colored printed false positives.

**Acceptance:** Separate blue/red masks and extracted candidate images. Do not label them authenticated signatures/stamps.

### Phase 6 — HUD and controls (Week 4)
**Objective:** Build usable multi-view inspection.

- [ ] **6.1** Display live tracker, Canny edges, rectified scan, and extracted marks.
- [ ] **6.2** Display detection state and measured FPS/latency.
- [ ] **6.3** Implement `C` to capture/freeze a valid document.
- [ ] **6.4** Implement `R` to resume live tracking.
- [ ] **6.5** Implement `S` to save rectified/grayscale/enhanced scans.
- [ ] **6.6** Implement `E` to export masks and isolated color marks.
- [ ] **6.7** Implement `Q` to release webcam and exit.
- [ ] **6.8** Handle empty panels and unavailable detection gracefully.

**Acceptance:** All panels and controls work without blocking the camera loop.

### Phase 7 — Pipeline integration and stabilization (Week 4–5)
**Objective:** Connect modules with clear data contracts.

- [ ] **7.1** Implement `src/pipeline.py` to coordinate stages.
- [ ] **7.2** Define outputs: original frame, edges, corners/status, warped image, enhanced scan, masks, marks, metrics.
- [ ] **7.3** Add corner smoothing (e.g., exponential moving average after consistent ordering).
- [ ] **7.4** Reset stale corner state on prolonged detection failure.
- [ ] **7.5** Ensure exports use one frozen capture, not mixed live frames.
- [ ] **7.6** Implement `src/exporter.py` with unique capture IDs and error handling.
- [ ] **7.7** Add integration tests on static sample images.

**Acceptance:** Complete capture → detection → rectification → enhancement/extraction → display/export flow works repeatedly.

### Phase 8 — Validation and optimization (Week 5–6)
**Objective:** Quantify quality and speed.

- [ ] **8.1** Collect representative sample images/video with varied lighting, tilt, background, ink colors, and occlusions.
- [ ] **8.2** Manually annotate document corners and representative color-mark masks.
- [ ] **8.3** Measure document detection rate and corner error.
- [ ] **8.4** Measure segmentation precision, recall, F1/IoU against annotated masks.
- [ ] **8.5** Measure mean, median, and p95 processing latency and sustained FPS.
- [ ] **8.6** Profile slow stages and optimize resolution, contour filtering, copies, and conversions.
- [ ] **8.7** Test missing webcam, unreadable frames, no document, and unwritable output path.
- [ ] **8.8** Record hardware, camera resolution, parameter settings, and observed failures.

**Acceptance:** Reproducible benchmark results; performance claims match measurements.

### Phase 9 — Documentation and final delivery (Week 6)
**Objective:** Make the application demonstrable and maintainable.

- [ ] **9.1** Complete README with prerequisites, setup, usage, controls, and troubleshooting.
- [ ] **9.2** Pin tested dependency versions in `requirements.txt`.
- [ ] **9.3** Add architecture diagram and explanation of 3×3 homography.
- [ ] **9.4** Document adaptive thresholding and HSV ranges.
- [ ] **9.5** Add screenshots of all diagnostic panels.
- [ ] **9.6** Record demonstration with detection, correction, scan, extraction, and export.
- [ ] **9.7** Include measured FPS/accuracy and known limitations.
- [ ] **9.8** Review code structure, tests, and Git history.

**Acceptance:** Another developer can install, run, test, and reproduce the demonstration.

## 4. Optional Phase 10 — PySide6 desktop UI
Only after the OpenCV MVP is stable:
- [ ] Install PySide6 and create a four-panel main window.
- [ ] Move frame acquisition/processing to a worker thread.
- [ ] Use signals/slots to update image panels safely.
- [ ] Add camera selector, capture/export controls, status bar, HSV sliders.
- [ ] Verify clean thread shutdown and UI responsiveness.

## 5. Suggested interfaces between modules
```python
# camera.py
read_frame() -> np.ndarray | None

# preprocessing.py
preprocess(frame: np.ndarray) -> tuple[np.ndarray, np.ndarray]

# document_detector.py
detect_document(edges: np.ndarray) -> np.ndarray | None  # shape (4, 2)

# perspective.py
rectify_document(frame: np.ndarray, corners: np.ndarray) -> np.ndarray

# enhancement.py
enhance_document(warped_bgr: np.ndarray) -> dict  # grayscale, binary

# color_extractor.py
extract_color_marks(warped_bgr: np.ndarray) -> dict  # masks, marks

# exporter.py
save_capture(capture_data: dict, output_dir: str) -> str
```
These are proposed contracts; refine return types and errors during implementation.

## 6. Test matrix
| Scenario | Detection | Rectification | Enhancement | Color extraction |
|---|---|---|---|---|
| Flat white page, good light | Baseline | Baseline | Baseline | Baseline |
| Tilted page | Check corners | Check geometry | Check legibility | Check alignment |
| Shadow across page | Check boundary | Check geometry | Check contrast | Check color stability |
| Cluttered background | False positives | Only if detected | N/A if missing | N/A if missing |
| Blue signature | Check | Check | Thin stroke retention | Blue recall |
| Red stamp | Check | Check | Stamp preservation | Red recall |
| Blue printed logo | Check | Check | Check | False-positive behavior |
| Hand partly covers edge | Recovery/failure state | Avoid invalid warp | N/A if missing | N/A if missing |
| No page in view | Explicit no detection | No warp | No output | No output |

## 7. Milestones
| Milestone | Deliverable | Target |
|---|---|---|
| M1 | Live camera + detected quadrilateral | End of Week 1 |
| M2 | Rectified and enhanced scan | End of Week 2 |
| M3 | Blue/red extracted masks and images | End of Week 3 |
| M4 | Interactive HUD and export | End of Week 4 |
| M5 | Benchmarks, robustness, documentation | End of Week 6 |

## 8. Immediate next actions
1. Set up virtual environment and verify webcam input.
2. Commit the first working camera loop.
3. Implement preprocessing and display the Canny edge map.
4. Add contour selection and overlay four corners.
5. Test with at least three documents/backgrounds before starting homography.

## 9. Engineering rules
- Never warp with missing, repeated, or degenerate corners.
- Keep original rectified color pixels for HSV segmentation; do not segment the binary scan.
- Separate UI rendering from CV processing logic.
- Record benchmark conditions; never present target FPS as measured FPS.
- Preserve unmodified inputs and raw masks when debugging.
- Treat HSV outputs as color-selected mark candidates, not proof of authenticity.
