from direct.gui.OnscreenImage import OnscreenImage  # Імпорт класу для роботи з зображеннями на екрані
from panda3d.core import TransparencyAttrib  # Імпорт атрибута прозорості
from panda3d.core import WindowProperties  # Імпорт класу для налаштування вікна
from direct.showbase.ShowBase import ShowBase  # Імпорт базового класу для гри
from panda3d.core import CollisionTraverser, CollisionNode, CollisionRay, CollisionHandlerQueue  # Імпорт класів для обробки колізій
from direct.gui.OnscreenImage import OnscreenImage  # Імпорт класу для роботи з зображеннями на екрані
from panda3d.core import BitMask32  # Імпорт класу для бітових масок

# Клавіші для управління
key_switch_camera = 'c'  # Перемикання камери
key_switch_mode = 'z'  # Перемикання режиму

key_forward = 'w'  # Вперед
key_back = 's'  # Назад
key_left = 'a'  # Вліво
key_right = 'd'  # Вправо
key_up = 'e'  # Вгору
key_down = 'q'  # Вниз

class Hero():  # Оголошення класу героя
    def __init__(self, pos, land):  # Конструктор класу
        self.land = land  # Зберігання інформації про землю
        self.mode = True  # Режим проходження сквозь об'єкти
        self.hero = loader.loadModel('steve.glb')  # Завантаження моделі героя
        self.hero.setScale(0.1)  # Встановлення масштабу
        self.hero.setPos(pos)  # Встановлення позиції
        self.hero.setHpr(0, 90, 0)  # Встановлення орієнтації
        self.hero.reparentTo(render)  # Додавання героя до сцени

        self.cameraBind()  # Прив'язка камери до героя
        self.accept_events()  # Прийом подій управління

        # Ініціалізація типів блоків
        self.grass_block = 'grass-block.glb'  # Блок трави
        self.dirt_block = "dirt-block.glb"  # Блок землі
        self.stone_block = "stone-block.glb"  # Блок каменю
        self.selectedBlockType = self.grass_block  # Обраний тип блоку

        # Ініціалізація детекції колізій
        self.rayQueue = CollisionHandlerQueue()  # Черга обробки колізій
        self.traverser = CollisionTraverser()  # Переміщувач колізій

        # Створення колізійного променя
        ray = CollisionRay()  # Створення нового променя
        ray.setOrigin(0, 0, 0)  # Початкова точка променя
        ray.setDirection(0, 1, 0)  # Напрямок променя (попереду камери)

        rayNode = CollisionNode('ray')  # Створення вузла колізії
        rayNode.addSolid(ray)  # Додавання променя до вузла
        rayNode.setFromCollideMask(BitMask32.bit(1))  # Встановлення маски колізії

        self.rayNodePath = base.camera.attachNewNode(rayNode)  # Прив'язка вузла променя до камери
        self.traverser.addCollider(self.rayNodePath, self.rayQueue)  # Додавання колізії до переміщувача

        # Включення візуалізації колізій (необов'язково)
        self.rayNodePath.show()

    def get_position(self):
        return self.hero.getPos()  # Метод для отримання позиції героя

    def cameraBind(self):
        base.disableMouse()  # Вимкнення миші
        base.camera.setHpr(90, 90, 90)  # Встановлення орієнтації камери
        crosshairs = OnscreenImage(  # Створення перехрестя на екрані
            image='crosshairs.png',
            pos=(0, 0, 0),
            scale=0.05,
        )

        crosshairs.setTransparency(TransparencyAttrib.MAlpha)  # Встановлення прозорості

        base.camera.reparentTo(self.hero)  # Прив'язка камери до героя
        base.camera.setPos(5, 8, 30)  # Встановлення позиції камери
        props = WindowProperties()
        props.setCursorHidden(0)  # Приховати курсор
        props.setMouseMode(WindowProperties.M_confined)  # Захопити курсор в межах вікна
        base.win.requestProperties(props)  # Застосувати налаштування
        self.mouseLookEnabled = True  # Увімкнення управління мишкою

        taskMgr.add(self.mouseLookTask, "mouseLookTask")  # Додати завдання для обробки миші
        self.cameraOn = True  # Камера активна

    def cameraUp(self):
        pos = self.hero.getPos()  # Отримати позицію героя
        base.mouseInterfaceNode.setPos(0, 0, 0)  # Скидання позиції вузла миші
        base.camera.reparentTo(render)  # Повернення камери до сцени
        base.enableMouse()  # Увімкнення миші
        props = WindowProperties()
        props.setCursorHidden(False)  # Показати курсор
        base.win.requestProperties(props)  # Застосувати налаштування
        self.hero.setHpr(0, 90, 0)  # Встановлення орієнтації героя

        self.mouseLookEnabled = False  # Вимкнення управління мишкою
        self.cameraOn = False  # Камера неактивна
        taskMgr.remove("mouseLookTask")  # Видалення завдання обробки миші

    def changeView(self):
        # Перемикання між режимами камери
        if self.cameraOn:
            self.cameraUp()
        else:
            self.cameraBind()

    def mouseLookTask(self, task):
        # Обробка руху миші
        if self.mouseLookEnabled and base.mouseWatcherNode.hasMouse():
            mouseX = base.win.getPointer(0).getX()  # Отримання координати X миші
            mouseY = base.win.getPointer(0).getY()  # Отримання координати Y миші

            # Обчислення зміщення миші від центру
            winXhalf = base.win.getXSize() // 2
            winYhalf = base.win.getYSize() // 2

            deltaX = mouseX - winXhalf  # Зміщення по осі X
            deltaY = mouseY - winYhalf  # Зміщення по осі Y

            # Обертання героя в залежності від руху миші
            self.hero.setH(self.hero.getH() - deltaX * 0.1)  # Обертання по горизонталі
            self.hero.setP(self.hero.getP() - deltaY * (-0.1))  # Обертання по вертикалі

            # Повернути курсор у центр екрану
            base.win.movePointer(0, winXhalf, winYhalf)

        return task.cont  # Продовжити завдання

    def look_at(self, angle):
        # Обчислення нової позиції в залежності від кута
        x_from = round(self.hero.getX())
        y_from = round(self.hero.getY())
        z_from = round(self.hero.getZ())

        dx, dy = self.check_dir(angle)  # Перевірка напрямку
        x_to = x_from + dx  # Нова координата X
        y_to = y_from + dy  # Нова координата Y
        return x_to, y_to, z_from  # Повернення нової позиції

    def just_move(self, angle):
        # Переміщення героя на нову позицію
        pos = self.look_at(angle)
        self.hero.setPos(pos)

    def move_to(self, angle):
        # Переміщення в залежності від режиму
        if self.mode:
            self.just_move(angle)
        else:
            self.try_move(angle)  # Спроба переміщення в іншому режимі

    def check_dir(self, angle):
        # Перевірка напрямку руху в залежності від кута
        if angle >= 0 and angle <= 20:
            return (0, -1)  # Вперед
        elif angle <= 65:
            return (1, -1)  # Вперед вправо
        elif angle <= 110:
            return (1, 0)  # Вправо
        elif angle <= 155:
            return (1, 1)  # Вправо назад
        elif angle <= 200:
            return (0, 1)  # Назад
        elif angle <= 245:
            return (-1, 1)  # Назад вліво
        elif angle <= 290:
            return (-1, 0)  # Вліво
        elif angle <= 335:
            return (-1, -1)  # Вліво вперед
        else:
            return (0, -1)  # Вперед

    def try_move(self, angle):
        # Спроба переміщення з обробкою колізій
        x_to, y_to, z_to = self.look_at(angle)  # Отримати нову позицію
        self.rayNodePath.setPos(self.hero.getPos())  # Встановити позицію променя
        self.rayNodePath.lookAt(x_to, y_to, z_to)  # Встановити напрямок променя
        self.traverser.traverse(render)  # Обробити колізії

        # Перевірка наявності колізій
        if self.rayQueue.getNumEntries() > 0:  # Якщо колізії є
            self.rayQueue.sortEntries()  # Сортування колізій
            entry = self.rayQueue.getEntry(0)  # Отримати перший запис
            if entry.getIntoNode().getName() == 'ground':  # Якщо колізія з землею
                # Встановити нову позицію
                self.hero.setPos(self.hero.getPos() + entry.getSurfaceNormal(render) * 0.1)
        else:
            self.just_move(angle)  # Просто перемістити


    def forward(self):
        # Отримуємо поточний кут обертання героя і викликаємо метод переміщення вперед
        angle = (self.hero.getH()) % 360
        self.move_to(angle)

    def back(self):
        # Обчислюємо кут для переміщення назад і викликаємо метод переміщення
        angle = (self.hero.getH() + 180) % 360
        self.move_to(angle)

    def left(self):
        # Обчислюємо кут для переміщення вліво і викликаємо метод переміщення
        angle = (self.hero.getH() + 90) % 360
        self.move_to(angle)

    def right(self):
        # Обчислюємо кут для переміщення вправо і викликаємо метод переміщення
        angle = (self.hero.getH() + 270) % 360
        self.move_to(angle)

    def changeMode(self):
        # Перемикаємо режим проходження
        self.mode = not self.mode  # Змінюємо значення режиму

    def up(self):
        # Якщо режим проходження активний, піднімаємо героя вгору
        if self.mode:
            self.hero.setZ(self.hero.getZ() + 1)

    def captureMouse(self):
        # Активуємо управління мишкою для камери
        self.cameraSwingActivated = True

        md = base.win.getPointer(0)  # Отримуємо позицію миші
        self.lastMouseX = md.getX()  # Зберігаємо координату X
        self.lastMouseY = md.getY()  # Зберігаємо координату Y

        properties = WindowProperties()
        properties.setCursorHidden(True)  # Приховуємо курсор
        properties.setMouseMode(WindowProperties.M_relative)  # Увімкнення відносного режиму миші
        base.win.requestProperties(properties)  # Застосовуємо нові властивості вікна

    def handleLeftClick(self):
        # Обробка лівого кліку миші
        self.captureMouse()  # Захоплюємо мишу
        self.removeBlock()  # Видаляємо блок

    def removeBlock(self):
        # Обробка видалення блоку
        self.traverser.traverse(render)  # Обробляємо колізії в сцені

        if self.rayQueue.getNumEntries() > 0:  # Якщо є колізії
            self.rayQueue.sortEntries()  # Сортуємо колізії
            rayHit = self.rayQueue.getEntry(0)  # Отримуємо перший запис колізії

            hitNodePath = rayHit.getIntoNodePath()  # Отримуємо шлях до об'єкта, з яким сталася колізія
            hitObject = hitNodePath.getPythonTag('owner')  # Отримуємо об'єкт, з яким сталася колізія

            if hitObject:
                distanceFromPlayer = hitObject.getDistance(self.hero)  # Відстань до героя
                print(distanceFromPlayer)
                if distanceFromPlayer < 120:  # Якщо відстань менше 12 одиниць
                    hitNodePath.clearPythonTag('owner')  # Очищуємо тег власника
                    hitObject.removeNode()  # Видаляємо об'єкт

    def placeBlock(self):
        # Обробка розміщення блоку
        self.traverser.traverse(render)  # Обробляємо колізії в сцені

        if self.rayQueue.getNumEntries() > 0:  # Якщо є колізії
            self.rayQueue.sortEntries()  # Сортуємо колізії
            rayHit = self.rayQueue.getEntry(0)  # Отримуємо перший запис колізії

            hitNodePath = rayHit.getIntoNodePath()  # Отримуємо шлях до об'єкта, з яким сталася колізія
            normal = rayHit.getSurfaceNormal(hitNodePath)  # Нормаль поверхні

            hitObject = hitNodePath.getPythonTag('owner')  # Отримуємо об'єкт, з яким сталася колізія
            if hitObject:
                # distanceFromPlayer = hitObject.getDistance(self.hero)  # Відстань до героя
                # if distanceFromPlayer < 140:  # Якщо відстань менше 14 одиниць
                    hitBlockPos = hitObject.getPos()  # Отримуємо позицію блоку
                    newBlockPos = hitBlockPos + normal * 2  # Обчислюємо нову позицію для розміщення блоку
                    self.land.add_block((newBlockPos.x, newBlockPos.y, newBlockPos.z+2), self.grass_block)  # Створюємо новий блок

    def down(self):
        # Якщо режим проходження активний і герой вище 1 одиниці, опускаємо героя вниз
        if self.mode and self.hero.getZ() > 1:
            self.hero.setZ(self.hero.getZ() - 1)

    def accept_events(self):
        # Прийом подій управління
        base.accept(key_forward, self.forward)  # Вперед
        base.accept(key_forward + '-repeat', self.forward)  # Повторне натискання вперед
        base.accept(key_back, self.back)  # Назад
        base.accept(key_back + '-repeat', self.back)  # Повторне натискання назад
        base.accept(key_left, self.left)  # Вліво
        base.accept(key_left + '-repeat', self.left)  # Повторне натискання вліво
        base.accept(key_right, self.right)  # Вправо
        base.accept(key_right + '-repeat', self.right)  # Повторне натискання вправо

        base.accept(key_switch_camera, self.changeView)  # Перемикання камери

        base.accept('mouse1', self.handleLeftClick)  # Лівий клік миші для видалення
        base.accept('mouse3', self.placeBlock)  # Правий клік миші для розміщення блоку
        base.accept(key_switch_mode, self.changeMode)  # Перемикання режиму

        base.accept(key_up, self.up)  # Вгору
        base.accept(key_up + '-repeat', self.up)  # Повторне натискання вгору
        base.accept(key_down, self.down)  # Вниз
        base.accept(key_down + '-repeat', self.down)  # Повторне натискання вниз
