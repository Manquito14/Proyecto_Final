import random
import time
import discord
from discord.ext import commands
from trivia import trivia_cambio_climatico

permisos = discord.Intents.default()
permisos.message_content = True

ecoco = commands.Bot(command_prefix="/", intents=permisos)


@ecoco.event
async def on_ready():
    """
    Aviso del estado de inicio del bot.
    """
    print(f"{ecoco.user} está en linea")


@ecoco.command()
async def hola(ctx):
    """
    Guía sobre cuales comandos y su uso.
    """
    await ctx.send("¡Hola! Soy Ecoco. \n Comandos:\n /hola  |  Te daré información sobre mis comandos y sus usos.\n /Trivia  |  Te haré una pregunta aleatoria sobre el cambio climático.")


@ecoco.command()
async def trivia(ctx):
    """
    Inicio y selección de la pregunta.
    """
    await ctx.send("👀 ¿Estás listo para la trivia? Comencemos entonces en...")
    time.sleep(2)
    await ctx.send("3")
    time.sleep(1)
    await ctx.send("2")
    time.sleep(1)
    await ctx.send("1")
    time.sleep(1)

    seleccion_de_pregunta = trivia_cambio_climatico[random.randint(1, len(trivia_cambio_climatico))]

    class TriviaBoton(discord.ui.View):
        """
        Muestra de las opciones de respuesta en el chat.
        """
        def __init__(self):
            super().__init__(timeout=None)

        @discord.ui.button(label=seleccion_de_pregunta["opciones"][0], style=discord.ButtonStyle.primary)
        async def opcion_1(self, button, interaction):
            await self.revision_de_respuesta(button, interaction)

        @discord.ui.button(label=seleccion_de_pregunta["opciones"][1], style=discord.ButtonStyle.primary)
        async def opcion_2(self, button, interaction):
            await self.revision_de_respuesta(button, interaction)

        @discord.ui.button(label=seleccion_de_pregunta["opciones"][2], style=discord.ButtonStyle.primary)
        async def opcion_3(self, button, interaction):
            await self.revision_de_respuesta(button, interaction)

        async def revision_de_respuesta(self, interaction, button):
            """
            Corrección o validación de la pregunta + dato curioso.
            """
            respuesta_correcta = seleccion_de_pregunta["opciones"][seleccion_de_pregunta["respuesta_correcta"]]
            respuesta_usuario = button.label

            if respuesta_usuario == respuesta_correcta:
                button.style = discord.ButtonStyle.green
                await interaction.response.send_message(f"✅ ¡Correcto! {respuesta_correcta}\n💡 Dato Curioso: {seleccion_de_pregunta["dato_curioso"]}", ephemeral=False)
            elif respuesta_usuario != respuesta_correcta:
                button.style = discord.ButtonStyle.red
                await interaction.response.send_message(f"❌ Incorrecto. La respuesta era: {respuesta_correcta}\n💡 Dato Curioso: {seleccion_de_pregunta["dato_curioso"]}", ephemeral=False)

            for item in self.children:
                if isinstance(item, discord.ui.Button):
                    item.disabled = True
            await interaction.message.edit(view=self)

    await ctx.send("==============================================")
    await ctx.send(seleccion_de_pregunta["pregunta"], view=TriviaBoton())
    await ctx.send("==============================================")

ecoco.run("TOKEN")
