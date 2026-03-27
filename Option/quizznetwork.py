import flet as ft

# -------------------- QUESTIONS --------------------
questions = [
    {
        "question": "Que signifie TCP ?",
        "options": [
            "Transmission Control Protocol",
            "Transfer Communication Process",
            "Total Control Packet",
            "Transport Core Protocol"
        ],
        "answer": 0
    },
    {
        "question": "Quel protocole est utilisé pour naviguer sur le web ?",
        "options": ["FTP", "HTTP", "SMTP", "SSH"],
        "answer": 1
    },
    {
        "question": "Quel port est utilisé par défaut pour HTTPS ?",
        "options": ["80", "21", "443", "22"],
        "answer": 2
    },
    {
        "question": "Que fait un routeur ?",
        "options": [
            "Stocke des fichiers",
            "Connecte différents réseaux",
            "Affiche des pages web",
            "Crypte les données"
        ],
        "answer": 1
    },
    {
        "question": "Quelle couche du modèle OSI correspond au transport ?",
        "options": [
            "Couche 2",
            "Couche 3",
            "Couche 4",
            "Couche 7"
        ],
        "answer": 2
    }
]

# -------------------- APP --------------------

def main(page: ft.Page):
    page.title = "Network Quiz"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0f172a"

    score = 0
    current_q = 0

    question_text = ft.Text(size=28, weight="bold", color="white")
    feedback = ft.Text(size=18)
    options_column = ft.Column(spacing=15)
    progress = ft.ProgressBar(width=400, value=0)

    def update_question():
        options_column.controls.clear()
        feedback.value = ""

        q = questions[current_q]
        question_text.value = q["question"]
        progress.value = (current_q) / len(questions)

        for i, option in enumerate(q["options"]):
            btn = ft.Button(
                content=ft.Text(option, color="white"),
                width=400,
                height=50,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=12),
                    bgcolor="#1e293b"
                ),
                on_click=lambda e, i=i: check_answer(i)
            )
            options_column.controls.append(btn)

        page.update()

    def check_answer(selected):
        nonlocal score, current_q

        correct = questions[current_q]["answer"]

        if selected == correct:
            score += 1
            feedback.value = "✅ Bonne réponse"
            feedback.color = "green"
        else:
            feedback.value = "❌ Mauvaise réponse"
            feedback.color = "red"

        current_q += 1

        if current_q < len(questions):
            page.update()
            page.run_task(delayed_next)
        else:
            show_result()

    async def delayed_next():
        import asyncio
        await asyncio.sleep(1)
        update_question()

    def show_result():
        page.controls.clear()

        result = ft.Column(
            [
                ft.Text("Quiz terminé 🎉", size=40, weight="bold"),
                ft.Text(f"Score: {score}/{len(questions)}", size=30),
                ft.Button("Recommencer", on_click=restart)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        page.add(result)

    def restart(e):
        nonlocal score, current_q
        score = 0
        current_q = 0
        page.controls.clear()
        build_ui()

    def build_ui():
        container = ft.Container(
            content=ft.Column(
                [
                    question_text,
                    options_column,
                    feedback,
                    progress
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=25
            ),
            padding=30,
            border_radius=20,
            bgcolor="#020617",
            width=500
        )

        page.add(
            ft.Row(
                [container],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True
            )
        )

        update_question()

    build_ui()