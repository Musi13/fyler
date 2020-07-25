# -*- mode: python ; coding: utf-8 -*-
import pkg_resources

block_cipher = None


# List of packages that should have there Distutils entrypoints included.
ep_package = 'fyler.providers'
hook_ep_packages = {ep_package: []}
hiddenimports = set()

for ep in pkg_resources.iter_entry_points(ep_package):
    hook_ep_packages[ep_package].append("{} = {}:{}".format(ep.name, ep.module_name, ep.attrs[0]))
    hiddenimports.add(ep.module_name)

    try:
        os.mkdir('./build')
    except FileExistsError:
        pass

    with open("./build/pkg_resources_hook.py", "w") as f:
        f.write("""# Runtime hook generated from spec file to support pkg_resources entrypoints.
ep_packages = {}

if ep_packages:
    import pkg_resources
    default_iter_entry_points = pkg_resources.iter_entry_points

    def hook_iter_entry_points(group, name=None):
        if group in ep_packages and ep_packages[group]:
            eps = ep_packages[group]
            for ep in eps:
                parsedEp = pkg_resources.EntryPoint.parse(ep)
                parsedEp.dist = pkg_resources.Distribution()
                yield parsedEp
        else:
            return default_iter_entry_points(group, name)

    pkg_resources.iter_entry_points = hook_iter_entry_points
""".format(hook_ep_packages))


def Entrypoint(dist, group, name, **kwargs):
    kwargs.setdefault('pathex', [])
    # get the entry point
    ep = pkg_resources.get_entry_info(dist, group, name)
    # insert path of the egg at the verify front of the search path
    kwargs['pathex'] = [ep.dist.location] + kwargs['pathex']
    # script name must not be a valid module name to avoid name clashes on import
    script_path = os.path.join(workpath, name + '-script.py')
    print("creating script for entry point", dist, group, name)
    with open(script_path, 'w') as fh:
        print("import", ep.module_name, file=fh)
        print("%s.%s()" % (ep.module_name, '.'.join(ep.attrs)), file=fh)

    return Analysis(
        [script_path] + kwargs.get('scripts', []),
        **kwargs
    )


a = Entrypoint(
    'fyler', 'gui_scripts', 'fyler',
    pathex=['/home/musi/Python/fyler'],
    binaries=[],
    datas=[('fyler/assets/*.ui', 'fyler/assets')],
    hiddenimports=list(hiddenimports),
    hookspath=[],
    runtime_hooks=['./build/pkg_resources_hook.py'],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='fyler',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )
