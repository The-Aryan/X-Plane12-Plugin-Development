from XPPython3 import xp # type: ignore

airspeed_ref = None
altitude_ref = None
vertical_speed_ref = None
n2_ref = None
n1_ref = None
n1_values = []

HUD_X = 50
HUD_Y = 500
LINE_SPACING = 20

def get_data():
    """Fetch aircraft parameters from X-Plane DataRefs."""
    xp.getDatavf(n1_ref, n1_values, count=2)
    return {
        "Airspeed": xp.getDataf(airspeed_ref),
        "Altitude": xp.getDataf(altitude_ref),
        "Vertical Speed": xp.getDataf(vertical_speed_ref),
        "N1A1": n1_values[0],
        "N1A2": n1_values[1]
    }

def flight_loop_callback(elapsed_since_last_call, elapsed_time_since_last_flight_loop, counter, refcon):
    """Refresh the HUD display every second."""
    xp.updateWidget(xp.NO_WIDGET)
    return 1.0

def draw_callback(inPhase, inIsBefore, inRefcon):
    """Draw HUD information on screen."""
    data = get_data()

    xp.drawTranslucentDarkBox(HUD_X - 10, HUD_Y + 15, HUD_X + 220, HUD_Y - 90)

    col_white = [1.0, 1.0, 1.0]
    col_green = [0.0, 1.0, 0.0]
    col_yellow = [1.0, 1.0, 0.0]
    col_red = [1.0, 0.0, 0.0]

    airspeed_color = col_green if data["Airspeed"] < 250 else col_yellow
    xp.drawString(airspeed_color, HUD_X, HUD_Y, f"Airspeed: {data['Airspeed']:.1f} kt", None, xp.Font_Basic)

    xp.drawString(col_white, HUD_X, HUD_Y - LINE_SPACING, f"Altitude: {data['Altitude']:.0f} ft", None, xp.Font_Basic)

    vs_color = col_green if abs(data["Vertical Speed"]) < 1000 else col_yellow
    xp.drawString(vs_color, HUD_X, HUD_Y - 2 * LINE_SPACING, f"V/S: {data['Vertical Speed']:.0f} fpm", None, xp.Font_Basic)

    n1a1_color = col_green if data["N1A1"] < 90 else col_red
    xp.drawString(n1a1_color, HUD_X, HUD_Y - 3 * LINE_SPACING, f"N1A1: {data['N1A1']:.0f}%", None, xp.Font_Basic)

    n1a2_color = col_green if data["N1A2"] < 90 else col_red
    xp.drawString(n1a2_color, HUD_X, HUD_Y - 4 * LINE_SPACING, f"N1A2: {data['N1A2']:.0f}%", None, xp.Font_Basic)

    return 1

class PythonInterface:
    def XPluginStart(self):
        global airspeed_ref, altitude_ref, vertical_speed_ref, throttle_ref, n2_ref, n1_ref
        
        # Find DataRefs
        airspeed_ref = xp.findDataRef("sim/flightmodel/position/indicated_airspeed")
        altitude_ref = xp.findDataRef("sim/cockpit2/gauges/indicators/altitude_ft_copilot")
        vertical_speed_ref = xp.findDataRef("sim/flightmodel/position/vh_ind_fpm")
        n2_ref = xp.findDataRef("sim/flightmodel/engine/ENGN_N2_")
        n1_ref = xp.findDataRef("sim/flightmodel/engine/ENGN_N1_")

        # Register Callbacks
        xp.registerFlightLoopCallback(flight_loop_callback, 1.0, None)
        xp.registerDrawCallback(draw_callback, xp.Phase_Window, 0, None)

        return "FlightStatusHUD", "com.myplugin.fshud", "Displays flight data as a HUD overlay"

    def XPluginEnable(self):
        return 1

    def XPluginDisable(self):
        xp.unregisterFlightLoopCallback(flight_loop_callback)
        xp.unregisterDrawCallback(draw_callback)

    def XPluginStop(self):
        return

# from XPPython3 import xp

# # DataRef for Vertical Speed
# vertical_speed_ref = None

# # Scale Dimensions
# VS_SCALE_X = 800  # Position on screen
# VS_SCALE_Y = 400
# SCALE_HEIGHT = 200  # Full height of the VS scale
# TICK_SPACING = 20   # Distance between ticks

# def draw_vs_scale():
#     """Draws a Vertical Speed Scale with dynamic markers."""
#     vs_value = xp.getDataf(vertical_speed_ref)

#     # Background for scale
#     xp.drawTranslucentDarkBox(VS_SCALE_X - 40, VS_SCALE_Y + SCALE_HEIGHT // 2,
#                               VS_SCALE_X + 40, VS_SCALE_Y - SCALE_HEIGHT // 2)

#     # Draw Zero Line (Center)
#     xp.drawLine(VS_SCALE_X - 20, VS_SCALE_Y, VS_SCALE_X + 20, VS_SCALE_Y, [1.0, 1.0, 1.0])  # White Line

#     # Scale Markers
#     for i in range(-SCALE_HEIGHT // 2, SCALE_HEIGHT // 2, TICK_SPACING):
#         tick_color = [0.0, 1.0, 0.0] if abs(i) < 60 else [1.0, 1.0, 0.0] if abs(i) < 140 else [1.0, 0.0, 0.0]
#         xp.drawLine(VS_SCALE_X - 10, VS_SCALE_Y + i, VS_SCALE_X + 10, VS_SCALE_Y + i, tick_color)

#     # VS Pointer (Dynamic)
#     pointer_y = max(min(vs_value / 100, SCALE_HEIGHT // 2 - 10), -SCALE_HEIGHT // 2 + 10)
#     xp.drawLine(VS_SCALE_X - 15, VS_SCALE_Y + pointer_y, VS_SCALE_X + 15, VS_SCALE_Y + pointer_y, [1.0, 0.0, 0.0])

#     # Display Numerical Value
#     xp.drawString([1.0, 1.0, 1.0], VS_SCALE_X + 25, VS_SCALE_Y + pointer_y, f"{vs_value:.0f} fpm", None, xp.Font_Basic)

# def draw_callback(inPhase, inIsBefore, inRefcon):
#     """Main draw callback to render the scale on screen."""
#     draw_vs_scale()
#     return 1

# class PythonInterface:
#     def XPluginStart(self):
#         global vertical_speed_ref
#         vertical_speed_ref = xp.findDataRef("sim/flightmodel/position/vh_ind_fpm")

#         xp.registerDrawCallback(draw_callback, xp.Phase_Window, 0, None)
#         return "VSSCALE", "com.myplugin.vsscale", "Vertical Speed Scale Display"

#     def XPluginEnable(self):
#         return 1

#     def XPluginDisable(self):
#         xp.unregisterDrawCallback(draw_callback)

#     def XPluginStop(self):
#         return

#     def XPluginReceiveMessage(self, fromWho, message, param):
#         return
