import bpy
import requests
import datetime
import os

def save_scene_and_send_data(context):
    # Сохранение текущей сцены
    bpy.ops.wm.save_as_mainfile(filepath=bpy.path.abspath("//" + bpy.context.scene.name + ".blend"))

    # Получение имени пользователя и времени сохранения
    username = "Ваше имя пользователя"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Получение пути к сохраненному файлу
    filepath = bpy.path.abspath("//" + bpy.context.scene.name + ".blend")

    # Отправка POST-запроса на сервер
    url = "http://95.140.148.192:8000/api/save_scene/"
    data = {
        "username": username,
        "timestamp": timestamp,
        "filepath": filepath,
    }
    response = requests.post(url, data=data)

    # Обработка ответа от сервера
    if response.status_code == 200:
        print("Сцена успешно сохранена и данные отправлены на сервер.")
    else:
        print(f"Ошибка при отправке данных на сервер: {response.status_code}")

# Создание кнопки в Blender
bpy.types.Scene.save_and_send = bpy.props.StringProperty(
    name="Save & Send",
    description="Сохраняет текущую сцену и отправляет данные на сервер",
    default="Сохранить и отправить",
)

# Добавление панели в пользовательский интерфейс
class SAVE_SEND_PT_panel(bpy.types.Panel):
    bl_label = "Save & Send"
    bl_idname = "SAVE_SEND_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tools"

    def draw(self, context):
        layout = self.layout
        url = "http://95.140.148.192:8000/api/save_scene/"
        layout.operator("scene.save_and_send_operator", text="Save & Send")

# Создание оператора для вызова функции save_scene_and_send_data
class SaveAndSendOperator(bpy.types.Operator):
    bl_idname = "scene.save_and_send_operator"
    bl_label = "Save & Send"

    def execute(self, context):
        save_scene_and_send_data(context)
        return {'FINISHED'}

# Регистрация созданных классов
def register():
    bpy.utils.register_class(SAVE_SEND_PT_panel)
    bpy.utils.register_class(SaveAndSendOperator)

# Отключение созданных классов
def unregister():
    bpy.utils.unregister_class(SAVE_SEND_PT_panel)
    bpy.utils.unregister_class(SaveAndSendOperator)

# Выполнение регистрации
if __name__ == "__main__":
    register()
