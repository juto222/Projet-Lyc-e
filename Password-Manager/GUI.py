import flet as ft

def main(page: ft.Page):  # ← page est passé automatiquement par ft.app
    page.title = "Password Manager UI"
    page.theme_mode = "light"
    page.window_width = 1100
    page.window_height = 650
    page.padding = 0

    # Sidebar
    sidebar = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=80,
        min_extended_width=240,
        leading=ft.Column([
            ft.Text("VAULT", size=12, weight=ft.FontWeight.BOLD),
        ], spacing=20),
        destinations=[
            ft.NavigationRailDestination(
                icon="vpn_key",
                selected_icon="vpn_key",
                label="Passwords",
            ),
            ft.NavigationRailDestination(
                icon="note",
                selected_icon="note",
                label="Secure Notes",
            ),
            ft.NavigationRailDestination(
                icon="person",
                selected_icon="person",
                label="Personal Info",
            ),
            ft.NavigationRailDestination(
                icon="credit_card",
                selected_icon="credit_card",
                label="Payments",
            ),
        ],
    )

    # Password health card
    password_health_card = ft.Container(
        content=ft.Column([
            ft.Text("Password Health", size=20, weight=ft.FontWeight.BOLD),
            ft.Row([
                ft.Container(
                    width=150,
                    height=150,
                    bgcolor=ft.Colors.GREEN_100,
                    border_radius=10,
                    alignment=ft.alignment.center,
                    content=ft.Text("90", size=40, weight=ft.FontWeight.BOLD),
                ),
                ft.Column([
                    ft.Text("57 SAFE", size=16, color=ft.Colors.GREEN_600),
                    ft.Text("2 COMPROMISED", size=16, color=ft.Colors.RED_600),
                    ft.Text("3 REUSED", size=16, color=ft.Colors.ORANGE_600),
                    ft.Text("5 WEAK", size=16, color=ft.Colors.AMBER_600),
                ]),
            ], spacing=40),
            ft.ElevatedButton("Manage accounts", icon="settings"),
        ], spacing=20),
        padding=10,
        border_radius=12,
        bgcolor=ft.Colors.WHITE,
    )


    new_mdp = ft.Container(
        content=ft.ElevatedButton(
            text="Nouveau",
            icon="keyboard_arrow_down",
            ),
        alignment=ft.alignment.top_right,
        padding=20,
    )

    # Layout
    page.add(
        ft.Row([
            sidebar,
            ft.Container(
                expand=True,
                padding=20,
                content=ft.Column([
                    password_health_card,
                ], scroll=ft.ScrollMode.AUTO),
            ),
            new_mdp,
        ], expand=True)
    )

ft.app(target=main)  # ← Flet passe automatiquement la page
