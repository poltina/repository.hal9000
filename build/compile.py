# -*- coding: utf-8 -*-

import os
import hashlib
import zipfile

__author__ = 'hal9000'

XML = u"""
<addon id="repository.hal9000" name="HAL9000 Add-on Repository" version="1.0.1" provider-name="HAL9000">
    <extension point="xbmc.addon.repository" name="HAL9000 Add-on Repository">
        <info compressed="false">https://raw.githubusercontent.com/xbmc-addon/repository.hal9000/master/addons.xml</info>
        <checksum>https://raw.githubusercontent.com/xbmc-addon/repository.hal9000/master/addons.xml.md5</checksum>
        <datadir zip="true">https://raw.githubusercontent.com/xbmc-addon/repository.hal9000/master/repo</datadir>
    </extension>
    <extension point="xbmc.addon.metadata">
        <summary lang="en">Install HAL9000 Addons</summary>
        <description lang="en">Download and install addons by HAL9000</description>
        <summary lang="ru">Репозиторий HAL9000</summary>
        <description lang="ru">Скачивание и установка плагинов от HAL9000</description>
        <platform>all</platform>
    </extension>
</addon>
"""

def get_addons():
    addons = []
    for dirname in os.listdir('./repo'):
        if os.path.isdir('./repo/' + dirname):
            filelist = [x for x in os.listdir('./repo/' + dirname) if x.endswith('.zip')]
            if filelist:
                filelist.sort()
                filename = './repo/' + dirname + '/' + filelist.pop()
                z = zipfile.ZipFile(filename, 'r')
                addons.append('\n'.join([x for x in z.read(dirname + '/addon.xml').splitlines() if x.find('<?xml') == -1]))
                z.close()
                # for Kodi-17
                file(filename + '.md5', 'wb').write(hashlib.md5(file(filename, 'rb').read()).hexdigest())
    return addons


if __name__ == '__main__':
    addons = ['<?xml version="1.0" encoding="UTF-8"?>', '<addons>']
    addons.extend( get_addons() )
    addons.append(XML.encode('utf8'))
    addons.append('</addons>')
    
    file('./addons.xml', 'w').write('\n'.join(addons))
    file('./addons.xml.md5', 'w').write( hashlib.md5(file('./addons.xml', 'rb').read()).hexdigest() )

    file('./addon.xml', 'w').write('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' + XML.encode('utf8'))
    z = zipfile.ZipFile('./repository.hal9000.zip', 'w')
    z.write('./icon.png', 'repository.hal9000/icon.png')
    z.write('./addon.xml', 'repository.hal9000/addon.xml')
    z.close()
    os.unlink('./addon.xml')