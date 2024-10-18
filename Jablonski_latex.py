from manim import *
import numpy as np

class JablonskiDiagram(Scene):
    def construct(self):
        # Keeping default black background
        
        # Style configurations with thinner arrows and brighter colors
        styles = {
            "level": {"color": WHITE, "stroke_width": 1.5},
            "sublevel": {"color": WHITE, "stroke_width": 1, "dash_length": 0.1},
            "ionization": {"color": WHITE, "stroke_width": 1, "dash_length": 0.1},
            "transition": {"color": PURPLE, "stroke_width": 1.5},
            "radiative": {"color": RED_A, "stroke_width": 1.5},
            "nonradiative": {"color": BLUE_A, "stroke_width": 1.5, "dash_length": 0.1},
            "phosphorescence": {"color": GREEN_A, "stroke_width": 1.5},
            "fluoro": {"color": GREEN, "stroke_width": 2.5}
        }
        myBaseTemplate = TexTemplate(
            documentclass="\documentclass{article}"
        )
        myBaseTemplate.add_to_preamble(r"\usepackage{amsmath, amssymb, amsthm, graphicx}")
        
        # Improved scaling factor
        UNIT = 0.7
        
        def get_coords(x, y):
    # Center the diagram by adjusting the offset (increase for more centering)
            return np.array([x * UNIT - 1.5, y * UNIT - 3, 0])  # Adjust the -3.5 and -5 for centering

        
        # Create singlet energy levels with adjusted spacing
        singlet_levels = {
            "S00": get_coords(0, 0),
            "S10": get_coords(0, 4),
            "S20": get_coords(0, 6),
            "S30": get_coords(0, 8)
        }
        
        # Adjusted sublevel spacing
        sublevel_offset = get_coords(0, 0.4)[1] - get_coords(0, 0)[1]
        
        # Create all sublevels
        for base in ["S0", "S1", "S2"]:
            for i in range(1, 4):
                key = f"{base}{i}"
                base_key = f"{base}0"
                singlet_levels[key] = np.array([
                    singlet_levels[base_key][0],
                    singlet_levels[base_key][1] + i * sublevel_offset,
                    0
                ])
        
        # Create triplet levels with adjusted positioning
        triplet_levels = {
            # "T00": get_coords(7, 2.5),
            "T10": get_coords(7, 2.5),
            "T20": get_coords(7, 4.5)
        }
        
        # Create triplet sublevels
        for base in ["T1", "T2"]:
            for i in range(1, 4):
                key = f"{base}{i}"
                base_key = f"{base}0"
                triplet_levels[key] = np.array([
                    triplet_levels[base_key][0],
                    triplet_levels[base_key][1] + i * sublevel_offset,
                    0
                ])
        
        def create_level(start_x, end_x, y, style):
            if "dash_length" in style:
                dash_length = style.pop("dash_length")
                line = DashedLine(
                    start=get_coords(start_x, y/UNIT),
                    end=get_coords(end_x, y/UNIT),
                    dash_length=dash_length,
                    **style
                )
            else:
                line = Line(
                    start=get_coords(start_x, y/UNIT),
                    end=get_coords(end_x, y/UNIT),
                    **style
                )
            return line
        
        # Create main levels
        main_levels = VGroup()
        sublevel_lines = VGroup()
        
        # Create singlet levels
        for key, pos in singlet_levels.items():
            if key.endswith("0"):  # Main levels
                line = Line(start=pos + LEFT * 2, end=pos + RIGHT * 2, **styles["level"])
                label = Text(f"S{key[1]}", font_size=24, color=WHITE)
                label.next_to(line, LEFT, buff=0.3)
                main_levels.add(VGroup(line, label))
            else:  # Sublevels
                line = DashedLine(
                    start=pos + LEFT * 2,
                    end=pos + RIGHT * 2,
                    **styles["sublevel"]
                )
                sublevel_lines.add(line)
        
        # Create triplet levels
        for key, pos in triplet_levels.items():
            if key.endswith("0"):  # Main levels
                line = Line(start=pos + LEFT, end=pos + RIGHT, **styles["level"])
                label = Text(f"T{key[1]}", font_size=24, color=WHITE)
                label.next_to(line, RIGHT, buff=0.3)
                main_levels.add(VGroup(line, label))
            else:  # Sublevels
                line = DashedLine(
                    start=pos + LEFT,
                    end=pos + RIGHT,
                    **styles["sublevel"]
                )
                sublevel_lines.add(line)
        
        # Create ionization level
        ionization_y = get_coords(0, 9)[1]
        ionization = DashedLine(
            start=get_coords(-2, 9),
            end=get_coords(8, 9),
            **styles["ionization"]
        )
        ionization_label = Text("Ionization Limit", font_size=24, color=WHITE)
        ionization_label.next_to(ionization, LEFT, buff=0.3)
        
        # Improved arrow creation with precise positioning
# Improved arrow creation with precise positioning
        def create_transition_arrow(start, end, style, buff=0.05):
            return Arrow(
                start=start,
                end=end,
                buff=buff,
                tip_length=0.1,  # Smaller arrow head
                stroke_width=style["stroke_width"],
                color=style["color"]
            )
        
                # Create absorption transitions with improved positioning
        absorption_arrows = VGroup()
        base_start = singlet_levels["S00"]
        for i, end_key in enumerate(["S10", "S11", "S12", "S13", "S20", "S21", "S22", "S30"]):
            start = base_start + RIGHT * (i * 0.25)  # Slightly increased spacing for clarity
            end = singlet_levels[end_key] + UP * 0.1 + RIGHT * (i * 0.25) 
            arrow = create_transition_arrow(start, end, styles["transition"], buff=0.05)  # Reduced buffer
            absorption_arrows.add(arrow)
        
        # Create fluorescence transitions with improved positioning
        # Modify arrow heads for the curved arrows
# Create fluorescence transitions with smaller arrow heads
        fluorescence_arrows = VGroup()
        # base_start = singlet_levels["S10"] + LEFT * 0.5 
        base_start = singlet_levels["S10"]  + LEFT*0.5
        

        for i, end_key in enumerate(["S00", "S01", "S02", "S03"]):
            start = base_start + LEFT * (i * 0.3)# Adjusted horizontal placement
            end = singlet_levels[end_key] + LEFT * (i * 0.3) + LEFT*0.5
            
            # curve = CurvedArrow(
            #     start_point=start,
            #     end_point=end,
            #     angle=PI/5,  # Slightly increased angle for better separation
            #     color=styles["radiative"]["color"],
            #     stroke_width=styles["radiative"]["stroke_width"],
            #     tip_length=0.1  # Reduced arrowhead size for curved arrows
            # )
            # fluorescence_arrows.add(curve)
            arrow = create_transition_arrow(start, end, styles["fluoro"], buff=0.05)
            fluorescence_arrows.add(arrow)
        
        # Create intersystem crossing with improved positioning
        # Create intersystem crossing with smaller arrow heads
        isc = DashedVMobject(
            CurvedArrow(
                start_point=singlet_levels["S10"] + RIGHT * 2.2,  # Shifted start point for better clarity
                end_point=triplet_levels["T10"] + LEFT * 0.4,  # Adjusted endpoint
                angle=-PI/4,  # Sharper angle to avoid overlap
                color=styles["nonradiative"]["color"],
                stroke_width=styles["nonradiative"]["stroke_width"],
                tip_length=0.1  # Reduced arrowhead size for intersystem crossing
            ),
            num_dashes=25  # Increased number of dashes for a finer line
        )

        # Vibrational relaxation (non-radiative) arrows
        vibrational_relaxation_arrows = VGroup()
        # for base in ["S0", "S1", "S2"]:
        #     for i in range(1, 4):
        #         start = singlet_levels[f"{base}{i}"] + LEFT * (i * 0.3)
        #         end = singlet_levels[f"{base}{0}"] + LEFT * (i * 0.3)
        #         arrow = create_transition_arrow(start, end, styles["nonradiative"], buff=0.05)
        #         vibrational_relaxation_arrows.add(arrow)
        
        for base in ["T1", "T2"]:
            for i in range(1, 4):
                start = triplet_levels[f"{base}{i}"] + LEFT * (i * 0.1)
                end = triplet_levels[f"{base}{0}"] + LEFT * (i * 0.1)
                arrow = create_transition_arrow(start, end, styles["nonradiative"], buff=0.05)
                vibrational_relaxation_arrows.add(arrow)


        phosphorescence_arrows = VGroup()
        phosphorescence_start = triplet_levels["T10"]
        phosphorescence_end = singlet_levels["S00"]
        phosphorescence_arrow = create_transition_arrow(
            phosphorescence_start, phosphorescence_end, styles["phosphorescence"], buff=0.05
        )
        phosphorescence_arrows.add(phosphorescence_arrow)

        # Phosphorescence label
        phosphorescence_label = Text("Phosphorescence", font_size=24, color=GREEN_A)
        phosphorescence_label.shift(RIGHT*2.7, DOWN*2)

        # Animation sequence with improved timing
        self.play(
            *[Create(level) for level in main_levels],
            Create(ionization),
            Write(ionization_label),
            run_time=1.5
        )
        
        self.play(
            *[Create(sublevel) for sublevel in sublevel_lines],
            run_time=1.5
        )
        
        # Add labels
        singlet_label = Text("Singlet", font_size=24, color=WHITE).move_to(
            get_coords(2, 9.5)
        )
        triplet_label = Text("Triplet", font_size=24, color=WHITE).move_to(
            get_coords(7, 9.5)
        )
        
        self.play(
            Write(singlet_label),
            Write(triplet_label),
            run_time=1
        )
        
        # Animate transitions one by one for better visibility
        for arrow in absorption_arrows:
            self.play(Create(arrow), run_time=1)
        
        for arrow in fluorescence_arrows:
            self.play(Create(arrow), run_time=1)
        
        self.play(Create(isc), run_time=1)

        # Animate vibrational relaxation
        for arrow in vibrational_relaxation_arrows:
            self.play(Create(arrow), run_time=1)
        
        # Add process labels
        absorption_label = Tex("Absorption \\ $\sim 10^{-15}$ sec", font_size=20, color=WHITE).shift(RIGHT*0.8, DOWN)
        fluorescence_label = Tex("Fluorescence \\$\sim 10^{-9}$ sec ", font_size=20, color=WHITE).shift(LEFT*3.5, DOWN)
        isc_label = Text("Intersystem\ncrossing", font_size=20, color=WHITE).next_to(isc, UP*0.8)
        vib_rex_label = Text("Vibrational Relaxation", font_size=16, color=WHITE).shift(RIGHT*4.5, UP*0.7)
        
        self.play(
            Write(absorption_label),
            Write(fluorescence_label),
            Write(isc_label),
            Write(vib_rex_label),
            run_time=1
        )
        self.play(Create(phosphorescence_arrow), Write(phosphorescence_label), run_time=1.5)
        
        self.wait(2)

