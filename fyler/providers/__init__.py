import pkg_resources

all_providers = {
    k.name: k.load()() for k in
    pkg_resources.iter_entry_points('fyler.providers')
}
