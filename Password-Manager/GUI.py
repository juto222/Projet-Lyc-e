import flet as ft

def main(page: ft.Page):
    page.title = "Password Manager UI"
    page.theme_mode = "light"
    page.window_width = 1100
    page.window_height = 650
    page.padding = 0

    # Sidebar
    sidebar = ft.Container(
    width=220,
    bgcolor=ft.Colors.BLUE_700,
    padding=20,
    content=ft.Column(
        [
            ft.Text("VAULT", size=20, weight=ft.FontWeight.BOLD, color="white"),
            ft.Divider(color="white"),

            ft.ElevatedButton(
                content=ft.Row([ft.Icon("vpn_key", color="white"), ft.Text("Passwords", color="white")]),
                bgcolor=ft.Colors.BLUE_500,
                color="white",
            ),
            ft.ElevatedButton(
                content=ft.Row([ft.Icon("note", color="white"), ft.Text("Secure Notes", color="white")]),
                bgcolor=ft.Colors.BLUE_500,
                color="white",
            ),
            ft.ElevatedButton(
                content=ft.Row([ft.Icon("person", color="white"), ft.Text("Personal Info", color="white")]),
                bgcolor=ft.Colors.BLUE_500,
                color="white",
            ),
            ft.ElevatedButton(
                content=ft.Row([ft.Icon("credit_card", color="white"), ft.Text("Payments", color="white")]),
                bgcolor=ft.Colors.BLUE_500,
                color="white",
            ),
        ],
        spacing=15
    )
    )

    # Fonction pour une ligne de compte
    def account_row(logo, name, email):
        return ft.Container(
            padding=15,
                content=ft.Row([
                    ft.Checkbox(),
                    ft.Image(src=logo, width=30, height=30),
    
                    ft.Column([
                        ft.Text(name, size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_600),
                        ft.Text(email, size=13, color=ft.Colors.GREY_600),
                    ], spacing=1, expand=True),
    
                    ft.IconButton(icon="more_vert")
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                border=ft.border.only(bottom=ft.BorderSide(1, ft.Colors.GREY_300)),
        )

    # Colonne du contenu
    content_column = ft.Column(
        [
            account_row("logo.png", "Test Account", "test@example.com"),
            account_row("logo2.png", "Another Account", "hello@world.com"),
        ],
        scroll=ft.ScrollMode.AUTO,
        expand=True
    )

    # Bouton nouveau
    new_btn = ft.Container(
        content=ft.ElevatedButton(text="Nouveau", icon="add"),
        alignment=ft.alignment.top_right,
        padding=20,
    )

    # Layout global
    page.add(
        ft.Row(
            [
                sidebar,
                ft.Container(expand=True, padding=ft.padding.only(left=50),content=content_column),
                new_btn,
            ],
            expand=True
        )
    )


ft.app(target=main, view=ft.WEB_BROWSER)
