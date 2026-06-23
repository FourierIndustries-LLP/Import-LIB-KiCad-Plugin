# Created with strong reference to:
# https://github.com/uPesy/easyeda2kicad.py/blob/master/easyeda2kicad/__main__.py

import os
import logging

from easyeda2kicad.easyeda.easyeda_api import EasyedaApi
from easyeda2kicad.easyeda.parameters_easyeda import EeSymbol

from easyeda2kicad.easyeda.easyeda_importer import Easyeda3dModelImporter
from easyeda2kicad.easyeda.easyeda_importer import EasyedaFootprintImporter
from easyeda2kicad.easyeda.easyeda_importer import EasyedaSymbolImporter

from easyeda2kicad.kicad.export_kicad_3d_model import Exporter3dModelKicad
from easyeda2kicad.kicad.export_kicad_footprint import ExporterFootprintKicad
from easyeda2kicad.kicad.export_kicad_symbol import ExporterSymbolKicad
from easyeda2kicad.kicad.export_kicad_symbol import id_already_in_symbol_lib
from easyeda2kicad.kicad.export_kicad_symbol import write_component_in_symbol_lib_file


class easyeda2kicad_wrapper:
    def print(self, txt):
        print("\{LCSC\} " + txt)

    def import_Symbol(
        self,
        cad_data,
        output,
        overwrite=False,
        sym_lib_ext="kicad_sym",
        prefix="",
    ):
        importer = EasyedaSymbolImporter(easyeda_cp_cad_data=cad_data)
        easyeda_symbol: EeSymbol = importer.get_symbol()

        # Add prefix to symbol name and package name
        if len(prefix) > 0:
            easyeda_symbol.info.name = prefix + '_' + easyeda_symbol.info.name
            if easyeda_symbol.info.package:
                easyeda_symbol.info.package = prefix + '_' + easyeda_symbol.info.package

        lib_path = f"{output}.{sym_lib_ext}"

        is_id_already_in_symbol_lib = id_already_in_symbol_lib(
            lib_path=lib_path,
            component_name=easyeda_symbol.info.name,
        )

        if not overwrite and is_id_already_in_symbol_lib:
            self.print(
                "[info] Symbol already exists, please enable the overwrite option if you wish to update the older symbol"
            )
            return 1

        # The symbol format version is inferred from the existing library file.
        exporter = ExporterSymbolKicad(symbol=easyeda_symbol, lib_path=lib_path)
        kicad_symbol_lib = exporter.export(
            footprint_lib_name=output.split("/")[-1].split(".")[0],
        )

        # Writes the symbol into the library file, replacing it if it already exists.
        write_component_in_symbol_lib_file(
            lib_path=lib_path,
            component_name=easyeda_symbol.info.name,
            component_content=kicad_symbol_lib,
            version=exporter.version,
        )

        self.print(f"[info] Created Kicad symbol {easyeda_symbol.info.name}")
        print(f"[info] Library path : {lib_path}")

    def import_Footprint(
        self,
        cad_data,
        output,
        overwrite=False,
        lib_path_var="EASYEDA2KICAD",
        lib_name="Test_Unified_Lib",
        prefix="",
    ):
        # WARNING: the `output` parameter contains the full path to the library, and can only be used in the front
        importer = EasyedaFootprintImporter(easyeda_cp_cad_data=cad_data)
        easyeda_footprint = importer.get_footprint()

        # Add prefix to footprint name and 3D model entry inside the footprint
        if len(prefix) > 0:
            easyeda_footprint.info.name = prefix + '_' + easyeda_footprint.info.name
            if easyeda_footprint.model_3d is not None:
                easyeda_footprint.model_3d.name = prefix + '_' + easyeda_footprint.model_3d.name

        is_id_already_in_footprint_lib = os.path.isfile(
            f"{output}.pretty/{easyeda_footprint.info.name}.kicad_mod"
        )

        if not overwrite and is_id_already_in_footprint_lib:
            self.print(
                "[info] Footprint already exists, please enable the overwrite option if you wish to update the older footprint"
            )
            return 1

        ki_footprint = ExporterFootprintKicad(footprint=easyeda_footprint)
        footprint_filename = f"{easyeda_footprint.info.name}.kicad_mod"
        footprint_path = f"{output}.pretty"
        # model_3d_path = f"{output}.3dshapes".replace("\\", "/").replace("./", "/")

        # The path should look like ${KICAD_3RD_PARTY}/TESTING_library/TESTING_library.3dshapes/TQFP-64_L10.0-W10.0-H1.2-LS12.0-P0.50.wrl
        model_3d_path = f"${{{lib_path_var}}}/{lib_name}/{lib_name}.3dshapes"

        ki_footprint.export(
            footprint_full_path=f"{footprint_path}/{footprint_filename}",
            model_3d_path=model_3d_path,
        )

        self.print(f"[info] Created Kicad footprint {easyeda_footprint.info.name}")
        print(f"[info] Footprint path: {os.path.join(footprint_path, footprint_filename)}")

    def import_3D_Model(self, cad_data, output, prefix=""):
        model_3d = Easyeda3dModelImporter(
            easyeda_cp_cad_data=cad_data, download_raw_3d_model=True
        ).output
        exporter = Exporter3dModelKicad(model_3d=model_3d)

        # No 3D model available for this component.
        if not exporter.output:
            return

        # `export()` now writes the .wrl/.step files directly into the
        # given output directory (the .3dshapes folder).
        lib_path = f"{output}.3dshapes"
        exporter.export(output_dir=lib_path)

        model_name = exporter.output.name
        has_step = exporter.output_step is not None
        filename_wrl = f"{model_name}.wrl"
        filename_step = f"{model_name}.step"

        # The files are written unprefixed; rename them to add the prefix so
        # they match the prefixed reference stored inside the footprint.
        if len(prefix) > 0:
            name_with_prefix = prefix + '_' + model_name
            new_wrl_dir = os.path.join(lib_path, prefix + '_' + filename_wrl)
            new_step_dir = os.path.join(lib_path, prefix + '_' + filename_step)
            os.rename(os.path.join(lib_path, filename_wrl), new_wrl_dir)
            if has_step:
                os.rename(os.path.join(lib_path, filename_step), new_step_dir)
        else:
            name_with_prefix = model_name
            new_wrl_dir = os.path.join(lib_path, filename_wrl)
            new_step_dir = os.path.join(lib_path, filename_step)

        formats = "wrl"
        if has_step:
            formats += ",step"

        self.print(f"Created 3D model {name_with_prefix} ({formats})")
        print("3D model path (wrl): " + new_wrl_dir)
        if has_step:
            print("3D model path (step): " + new_step_dir)

    def full_import(
        self,
        component_id="",
        base_folder=False,
        overwrite=False,
        lib_name="Test_Unified_Lib",
        prefix="",
    ):
        base_folder = os.path.expanduser(base_folder)

        if not component_id.startswith("C"):
            self.print(
                "[error] LCSC Part Number should start with C.... example: C2040"
            )
            return False

        # Make the base folder, or the ${KICAD_3RD_PARTY} path
        if not os.path.isdir(base_folder):
            os.makedirs(base_folder, exist_ok=True)

        # Base folder is the full absolute path to the folder
        # lib_name is the name of the library itself, for the kicad_sym files and footprint .pretty folder
        output = f"{base_folder}/{lib_name}/{lib_name}"

        lib_var = "KICAD_3RD_PARTY"

        # Create new footprint folder if it does not exist
        if not os.path.isdir(f"{output}.pretty"):
            os.mkdir(f"{output}.pretty")
            self.print(
                f"[info] Created {lib_name}.pretty footprint folder in {base_folder}"
            )

        # Create new 3d model folder if it doesn't exist
        if not os.path.isdir(f"{output}.3dshapes"):
            os.mkdir(f"{output}.3dshapes")
            self.print(
                f"[info] Created {lib_name}.3dshapes 3D model folder in {base_folder}"
            )

        # Create symbol file if it doesn't exist
        lib_extension = "kicad_sym"
        if not os.path.isfile(f"{output}.{lib_extension}"):
            with open(
                file=f"{output}.{lib_extension}", mode="w+", encoding="utf-8"
            ) as my_lib:
                my_lib.write(
                    """\
                    (kicad_symbol_lib
                    (version 20211014)
                    (generator https://github.com/uPesy/easyeda2kicad.py)
                    )"""
                )
            self.print(f"Create {lib_name}.{lib_extension} symbol lib in {base_folder}")

        # Get CAD data of the component using easyeda API
        api = EasyedaApi()
        cad_data = api.get_cad_data_of_component(lcsc_id=component_id)

        # API returned no data
        if not cad_data:
            self.print(
                f"[error] Failed to fetch data from LCSC API for part {component_id}"
            )
            return 1

        # ---------------- SYMBOL ----------------
        self.import_Symbol(cad_data, output, overwrite=overwrite, prefix=prefix)
        # ---------------- FOOTPRINT -------------
        self.import_Footprint(
            cad_data,
            output,
            overwrite=overwrite,
            lib_path_var=lib_var,
            lib_name=lib_name,
            prefix=prefix
        )
        # ---------------- 3D MODEL --------------
        self.import_3D_Model(cad_data, output, prefix)
        return 0


if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR)
    base_folder = "~/Documents/Kicad/EasyEDA"
    easyeda_import = easyeda2kicad_wrapper()
    easyeda_import.full_import(component_id="C2040", base_folder=base_folder)
