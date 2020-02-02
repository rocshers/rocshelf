# ROCSHELF
Rocshelf - это препроцессор, работающий на python, компилирующий веб-страницы из отдельных частей с параллельной модернизацией.
За основу взята идея максимального разделение кода на независимые части, которые сливаются в единое целое при компиляции.


## Installation
Rocshelf импортирует и экспортирует файлы относительно своего расположения. Поэтому лучше всего расположить в корне вашего проекта
```bash
    cd your_project
    git clone https://github.com/rocshers/rocshelf.git
```

## Getting Started

В появившейся папке будет файл config.json в котором вам нужно указать расположение файлов для импорта, экспорта, маршруты и настройку обработчика.
```json
    "path": {
        "basic":    "source/basics/",
        "page":     "source/pages/",
        "tag":      "source/tags/",
        
        "static":   "ready/static/",
        "template": "ready/template/"
    },

    "routs": [
        "index"
    ],
    
    "setting": {
        "sass": "scss",
        "compression": " lvl0 / lvl1 / lvl2 / lvl3 "
    }
```

Введя следующую команду вы скрипт создаст папки из настройки "path" с примерами компонентов которые помогут вам разобраться в синтаксисе предпроцессора.
```bash
    cd rocshelf
    python3 __init__.py training
```
## Usage
Если вы воспользовались вышепредстваленной командой, то вы увидите три папки (basics, pages, tags). Rocshelf позволяет разбить ваш сайт на три части:
* **PAGE** - Основа любой страницы. В .html этого компонента указывается какой BASIC файл наследовать и какие TAG вызывать.
* **BASIC** - Обертка для PAGE. Самый верхний уровень иерархии компонентов.
* **TAG** - Мельчайший компонент, который может вызываться неоднократно и в разных местах кода.


## Tags
Для подключения TAG в коде страницы, не важно PAGE, BASIC или другого TAG, необходима следующая синтаксическая структура.
Обязательное условие для вызова это слово tag и имя TAG разделенные тире. При необходимости, через еще одно тире можно указывать тег.
```html
    <tag-name>  code...  </tag-name>
```
Она ссылается на элемент TAG с именем <code>name</code>. <br>
Если в .html файле данного элемента будет тег с такой же синтаксической структурой, они сольются.
Иной текст вставиться без изменения.
Слияние проходит так. Если в двух экземплярах не будет указан html тег то контент будет вставлен без тега. В ином случае приоритет тега будет отдан модификацией. Атрибуты оригинала так же заменяются модификацией, кроме классов, они соединяются. 

Если в тексте тега есть <code>{i{ content }}</code>, то она замениться на текст из модификации тега, без изменения окружающего наполнения. 
```html
    name/html.html
        <tag-name-div attrs>
            <span>{i{ content }}</span>
        </tag-name-div>

    =>
        <div attrs>
            <span>  code...  </span>
        </div>
```



## Structure
Шаблонизатор rocshelf может преобразовывать перечень конструкций для удобной работы с кодом.

### Merge BASIC and PAGE
При наличии <code>{merge{ basic_name }merge}</code> в файле PAGE и <code>{place{}merge}</code> в BASIC файле с именемем <code>basic_name</code> они сольются в единое. При их слиянии переменные становятся общими, то есть переменная указанная в PAGE будет вставлена в BASIC и наоборот. Но если будут общие, то PAGE будет перезаписывать их.
<br> Допускается использование нескольких merge на странице, но слияние будет происходить с последнего.

### SRC
Если какой-то элемент вашего сайта требует подключение сторонней библиотеки стилей или скриптов, вы можете задать их. При вызове данного элемента библиотеки автоматически загрузятся и обработаются с остальным кодом.
```html
     {src{ <!-- json format -->
        "script": {
            "prep": ["link"],
            "final": ["link"]
        },
        "style": {
            "prep": ["link"],
            "final": ["link"]
        }
    }src}
```


### Vars
Шаблонизатор поддерживает наличие переменных в коде. Они наследуются от большего к меньшему.
То есть заданная в BASIC переменная может применяться в других, добавленных позже, частях кода. Но, например, из тега в тег они не распространяются.
Переменные из BASIC и PAGE сливаются и распространяются на TAG, но переменные обЪявленные в PAGE перезаписывают переменные из BASIC.
ОбЪявить переменные можно с помощью структуры <code>{vars{ json_format }vars}</code>.
### Insert Vars
Для работы с переменными присутствуют все основные функции. <br>
**<code>{i{ name_var }}</code>** - данная структура заменяется переменной <code>name_var</code>. Если переменная не определена, то структура остается неизменной.
```html
    {for{
        {con{ i in list / dict }con}
        code ...
    }for}

    {if{
        {con{ True or False }con}

        {True{  code ... }True}
        {False{ code ... }False}
    }if}

    и т.д.
```
Конструкции InsertVars работают во всех фалах. Иные конструкции только в html.



### Prep-Prll-Final
Шаблонизатор разбивает код на три части. Первая загружается в самом начале, вторая параллельно html и третья в самом конце, после полной загрузки страницы. <br>
С помощью структур <code>Prep-Prll-Final</code> можно настроить загрузку страницы как вам удобно.
```
    .html 
        {prll{
            <style>/*Теперь стили будут подгружаться параллельно html*/</style> 
            <script>/*Теперь скрипты будут подгружаться параллельно html*/</script>
            При вызове участков кода для параллельной загрузки, они будут сливаться с теми, которые в данных тегах
        }prll}
        {final{ code... }final}

    .sass .js
        /*{prep{  code... }prep} */ - необязательно указывать для .sass
        /*{final{ code... }final}*/ - необязательно указывать для .js
        /*{prll{  code... }prll} */ 
```
Все обозначенные как предворительные файлы будут загруженны в <code><head></code>, а финальные, с помощью js, после загрузки html. 
<br>
<br>
<br>
## Development stage - v0.1
Проект находиться в стадии Pre-Alpha. <br>
Заложен фундамент принципа работы и инструменты для разработки.