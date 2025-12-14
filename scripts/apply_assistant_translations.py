#!/usr/bin/env python3
"""
Apply built-in assistant translations to TS files under geo_report/i18n.
This script uses an internal mapping (no external APIs) and updates <translation>
for each known source string. It preserves other XML structure.
"""
import xml.etree.ElementTree as ET
from pathlib import Path

I18N = Path('geo_report') / 'i18n'

TRANSLATIONS = {
    'fr': {
        'Layout Item Selector - geo_report': "Sélecteur d'éléments de mise en page - geo_report",
        'Layout List:': 'Liste des mises en page :',
        'Scale:': 'Échelle :',
        'Angle:': 'Angle :',
        'Show Print Area on Map': "Afficher la zone d'impression sur la carte",
        'Open Layout Manager': 'Ouvrir le gestionnaire de mise en page',
        'Refresh Item Info': "Actualiser les informations de l'élément",
        'Save Layout': 'Enregistrer la mise en page',
        'Load Layout': 'Charger la mise en page',
        'Cancel': 'Annuler',
        'Layout Items:': 'Éléments de mise en page :',
        'Item Name': "Nom de l'élément",
        'Type': 'Type',
        'Visible': 'Visible',
        'Item Properties': "Propriétés de l'élément",
        'Selected Item Properties:': "Propriétés de l'élément sélectionné :",
        'Apply Properties': 'Appliquer les propriétés',
        'Layout Info': 'Infos de mise en page',
        'Layout Information:': 'Informations sur la mise en page :',
    },
    'de': {
        'Layout Item Selector - geo_report': 'Layout-Element-Auswahl - geo_report',
        'Layout List:': 'Layout-Liste:',
        'Scale:': 'Maßstab:',
        'Angle:': 'Winkel:',
        'Show Print Area on Map': 'Druckbereich auf Karte anzeigen',
        'Open Layout Manager': 'Layoutmanager öffnen',
        'Refresh Item Info': 'Elementinformationen aktualisieren',
        'Save Layout': 'Layout speichern',
        'Load Layout': 'Layout laden',
        'Cancel': 'Abbrechen',
        'Layout Items:': 'Layout-Elemente:',
        'Item Name': 'Elementname',
        'Type': 'Typ',
        'Visible': 'Sichtbar',
        'Item Properties': 'Elementeigenschaften',
        'Selected Item Properties:': 'Ausgewählte Elementeigenschaften:',
        'Apply Properties': 'Eigenschaften anwenden',
        'Layout Info': 'Layout-Informationen',
        'Layout Information:': 'Layout-Informationen:',
    },
    'es': {
        'Layout Item Selector - geo_report': 'Selector de elementos de diseño - geo_report',
        'Layout List:': 'Lista de diseños:',
        'Scale:': 'Escala:',
        'Angle:': 'Ángulo:',
        'Show Print Area on Map': 'Mostrar área de impresión en el mapa',
        'Open Layout Manager': 'Abrir gestor de diseños',
        'Refresh Item Info': 'Actualizar información del elemento',
        'Save Layout': 'Guardar diseño',
        'Load Layout': 'Cargar diseño',
        'Cancel': 'Cancelar',
        'Layout Items:': 'Elementos del diseño:',
        'Item Name': 'Nombre del elemento',
        'Type': 'Tipo',
        'Visible': 'Visible',
        'Item Properties': 'Propiedades del elemento',
        'Selected Item Properties:': 'Propiedades del elemento seleccionado:',
        'Apply Properties': 'Aplicar propiedades',
        'Layout Info': 'Información del diseño',
        'Layout Information:': 'Información del diseño:',
    },
    'it': {
        'Layout Item Selector - geo_report': 'Selettore elementi layout - geo_report',
        'Layout List:': 'Elenco layout:',
        'Scale:': 'Scala:',
        'Angle:': 'Angolo:',
        'Show Print Area on Map': 'Mostra area di stampa sulla mappa',
        'Open Layout Manager': 'Apri gestore layout',
        'Refresh Item Info': 'Aggiorna informazioni elemento',
        'Save Layout': 'Salva layout',
        'Load Layout': 'Carica layout',
        'Cancel': 'Annulla',
        'Layout Items:': 'Elementi del layout:',
        'Item Name': 'Nome elemento',
        'Type': 'Tipo',
        'Visible': 'Visibile',
        'Item Properties': 'Proprietà elemento',
        'Selected Item Properties:': "Proprietà dell'elemento selezionato:",
        'Apply Properties': 'Applica proprietà',
        'Layout Info': 'Info layout',
        'Layout Information:': 'Informazioni sul layout:',
    },
    'pt': {
        'Layout Item Selector - geo_report': 'Seletor de itens de layout - geo_report',
        'Layout List:': 'Lista de layouts:',
        'Scale:': 'Escala:',
        'Angle:': 'Ângulo:',
        'Show Print Area on Map': 'Mostrar área de impressão no mapa',
        'Open Layout Manager': 'Abrir gerenciador de layout',
        'Refresh Item Info': 'Atualizar informações do item',
        'Save Layout': 'Salvar layout',
        'Load Layout': 'Carregar layout',
        'Cancel': 'Cancelar',
        'Layout Items:': 'Itens do layout:',
        'Item Name': 'Nome do item',
        'Type': 'Tipo',
        'Visible': 'Visível',
        'Item Properties': 'Propriedades do item',
        'Selected Item Properties:': 'Propriedades do item selecionado:',
        'Apply Properties': 'Aplicar propriedades',
        'Layout Info': 'Informações do layout',
        'Layout Information:': 'Informações do layout:',
    },
    'ja': {
        'Layout Item Selector - geo_report': 'レイアウト項目セレクタ - geo_report',
        'Layout List:': 'レイアウト一覧:',
        'Scale:': '縮尺:',
        'Angle:': '角度:',
        'Show Print Area on Map': '印刷領域を地図上に表示',
        'Open Layout Manager': 'レイアウトマネージャーを開く',
        'Refresh Item Info': '項目情報を更新',
        'Save Layout': 'レイアウトを保存',
        'Load Layout': 'レイアウトを読み込む',
        'Cancel': 'キャンセル',
        'Layout Items:': 'レイアウト項目:',
        'Item Name': '項目名',
        'Type': '種類',
        'Visible': '表示',
        'Item Properties': '項目プロパティ',
        'Selected Item Properties:': '選択項目のプロパティ:',
        'Apply Properties': 'プロパティ適用',
        'Layout Info': 'レイアウト情報',
        'Layout Information:': 'レイアウト情報:',
    },
    'zh': {
        'Layout Item Selector - geo_report': '布局项选择器 - geo_report',
        'Layout List:': '布局列表：',
        'Scale:': '比例：',
        'Angle:': '角度：',
        'Show Print Area on Map': '在地图上显示打印区域',
        'Open Layout Manager': '打开布局管理器',
        'Refresh Item Info': '刷新项目信息',
        'Save Layout': '保存布局',
        'Load Layout': '加载布局',
        'Cancel': '取消',
        'Layout Items:': '布局项：',
        'Item Name': '项名称',
        'Type': '类型',
        'Visible': '可见',
        'Item Properties': '项属性',
        'Selected Item Properties:': '所选项属性：',
        'Apply Properties': '应用属性',
        'Layout Info': '布局信息',
        'Layout Information:': '布局信息：',
    },
    'ru': {
        'Layout Item Selector - geo_report': 'Выбор элемента компоновки - geo_report',
        'Layout List:': 'Список компоновок:',
        'Scale:': 'Масштаб:',
        'Angle:': 'Угол:',
        'Show Print Area on Map': 'Показать область печати на карте',
        'Open Layout Manager': 'Открыть менеджер компоновок',
        'Refresh Item Info': 'Обновить информацию об элементе',
        'Save Layout': 'Сохранить компоновку',
        'Load Layout': 'Загрузить компоновку',
        'Cancel': 'Отмена',
        'Layout Items:': 'Элементы компоновки:',
        'Item Name': 'Имя элемента',
        'Type': 'Тип',
        'Visible': 'Видимый',
        'Item Properties': 'Свойства элемента',
        'Selected Item Properties:': 'Свойства выбранного элемента:',
        'Apply Properties': 'Применить свойства',
        'Layout Info': 'Информация о компоновке',
        'Layout Information:': 'Информация о компоновке:',
    },
    'hi': {
        'Layout Item Selector - geo_report': 'लेआउट आइटम चयनकर्ता - geo_report',
        'Layout List:': 'लेआउट सूची:',
        'Scale:': 'स्केल:',
        'Angle:': 'कोण:',
        'Show Print Area on Map': 'नक्शे पर प्रिंट क्षेत्र दिखाएँ',
        'Open Layout Manager': 'लेआउट प्रबंधक खोलें',
        'Refresh Item Info': 'आइटम जानकारी ताज़ा करें',
        'Save Layout': 'लेआउट सहेजें',
        'Load Layout': 'लेआउट लोड करें',
        'Cancel': 'रद्द करें',
        'Layout Items:': 'लेआउट आइटम:',
        'Item Name': 'आइटम नाम',
        'Type': 'प्रकार',
        'Visible': 'दृश्यमान',
        'Item Properties': 'आइटम गुण',
        'Selected Item Properties:': 'चयनित आइटम गुण:',
        'Apply Properties': 'गुण लागू करें',
        'Layout Info': 'लेआउट जानकारी',
        'Layout Information:': 'लेआउट जानकारी:',
    }
}


def apply_translations():
    for ts_file in sorted(I18N.glob('geo_report_*.ts')):
        lang = ts_file.stem.split('_')[-1]
        key = lang
        if key == 'zh_CN':
            key = 'zh'
        if key not in TRANSLATIONS and key != 'en':
            print(f'Skipping {ts_file.name}: no translations for language {key}')
            continue
        tree = ET.parse(ts_file)
        root = tree.getroot()
        changed = False
        for context in root.findall('context'):
            for message in context.findall('message'):
                src = message.find('source')
                trans = message.find('translation')
                if src is None:
                    continue
                stext = src.text or ''
                if key == 'en':
                    if trans is None:
                        trans = ET.SubElement(message, 'translation')
                    if trans.text != stext:
                        trans.text = stext
                        changed = True
                else:
                    tmap = TRANSLATIONS.get(key, {})
                    if stext in tmap:
                        newt = tmap[stext]
                        if trans is None:
                            trans = ET.SubElement(message, 'translation')
                        if trans.text != newt:
                            trans.text = newt
                            if 'type' in trans.attrib:
                                trans.attrib.pop('type')
                            changed = True
        if changed:
            tree.write(ts_file, encoding='utf-8', xml_declaration=True)
            print(f'Updated translations in {ts_file.name}')
        else:
            print(f'No changes for {ts_file.name}')


if __name__ == '__main__':
    apply_translations()
