# KiCad Import-LIB-KiCad-Plugin ![icon](plugins/icon_small.png)

![GitHub License](https://img.shields.io/github/license/FourierIndustries-LLP/Import-LIB-KiCad-Plugin)

> Easy to use KiCad library importer with a professional workflow

<div style="overflow:hidden; margin-top: 20px; margin-bottom: 20px;" align="center">
<img src="doc/FI_logo.jpeg" />
</div>

This plugin is a fork of the highly popular [Import-LIB-KiCad-Plugin](https://github.com/Steffen-W/Import-LIB-KiCad-Plugin), with an improved UI designed for a more professional KiCad library management workflow.

Download the plugin [here](https://github.com/FourierIndustries-LLP/Import-LIB-KiCad-Plugin/raw/refs/heads/master/Import-LIB-KiCad-Plugin.zip)!

## Design Philosophy

One of the major reasons why we forked the original plugin was the desire to create a library management framework for a collaborative, decentralised and shared KiCad library across a small to medium-sized organisation with standards based on the 3 Es:

- Easy to Access: accessing the latest version of the library should be a one-click or zero-click process (achieved through Git)
- Easy to Update: adding new parts or modifying parts in the ECAD library should be straightforward and simple (achieved through this plugin)
- Easy to Set up: the setup process should be as straightforward as possible to minimize errors during the setup process (achieved through good procedure)

All of the symbols, footprints and 3D models are placed in one custom-named library (with a single `.kicad_sym` file, a single `.pretty` footprints folder, and a single `.3dshapes` 3D models folder), giving you the flexibility to rapidly import and work with multiple libraries at the same time (for example, you can maintain a single company library and another library for personal use).

## Directories

* `doc/` - assets for documentation
* `plugins/` - source code
* `resource/` - assets included in the plugin

## Installation

Install this plugin using the KiCad Package Content Manager (PCM) with the "Install from File..." option.

## Setup

> Initial setup is **very important**!! This plugin will not work if initial setup is not carried out.

**Step 1**: Click on Configure Paths and add a new environment variable called `KICAD_3RD_PARTY`. This should be the folder where all of your third party libraries are placed.

<img src="doc/image.png" width=66% />

The folder structure inside `KICAD_3RD_PARTY` should look something like this:

```
KICAD_3RD_PARTY folder──┐                                                                                
                        ┼──My_Library_1─┬──My_Library_1.kicad_sym                                        
                        │               │                      ┌──Type_Manufacturer_Footprint_1.kicad_mod
                        │               ├──My_Library_1.pretty─┼                                         
                        │               │                      └──Type_Manufacturer_Footprint_2.kicad_mod
                        │               │                        ┌──Footprint_1.stp                      
                        │               └──My_Library_1.3dshapes─┼                                       
                        │                                        └──Footprint_2.stp                      
                        └──My_Library_2─┬──My_Library_2.kicad_sym                                        
                                        │                      ┌──Type_Manufacturer_Footprint_1.kicad_mod
                                        ├──My_Library_2.pretty─┼                                         
                                        │                      └──Type_Manufacturer_Footprint_2.kicad_mod
                                        │                        ┌──Footprint_1.stp                      
                                        └──My_Library_2.3dshapes─┼                                       
                                                                 └──Footprint_2.stp                                  
```

**Step 2**: Add the symbol library

Next, press the Manage Symbol Library button to bring up the Symbol Libraries window and press + to add the library name you want. The format of the library path must be

```
${KICAD_3RD_PARTY}/My_Library_1/My_Library_1.kicad_sym
```

where `My_Library_1` is the name of your library. 

<img src="doc/image-1.png" width=66% />


**Step 3**: Add the footprint library

Finally, press the Manage Footprint Library button to bring up the Footprint Libraries window and press + to add the library name you want. The format of the library path must be

```
${KICAD_3RD_PARTY}/My_Library_1/My_Library_1.pretty
```

where `My_Library_1` is the name of your library. 

<img src="doc/image-2.png" width=66% />

## Usage

### Adding a Samacsys/SnapEDA/Ultralibrarian/Octopart symbol/footprint ZIP file

Most symbols or footprints come from ZIP files made by these major ECAD component libraries. You can directly import those files as complete packages.

**Step 1**: Download the part from the source in the ZIP format

<img src="doc/image-3.png" width=66% />

**Step 2**: Open pcbnew (PCB editor interface) and click on the download icon to bring up the plugin

<img src="doc/image-4.png" width=66% />

**Step 3**: Make sure the radio button for the (manually download zip file) option is enabled, and select the zip file. Set a prefix if any, following the KiCad Library Convention (KLC) for naming symbols (e.g. Regulator_Linear_TI). Set the name of your library (e.g. `My_Library_1`), which is contained inside the `KICAD_3RD_PARTY` folder which you also have to specify here.

<img src="doc/image-5.png" width=66% />

**Step 4**: Press "Import!" and you're done!

### Adding an LCSC symbol/footprint

LCSC provides symbols, footprints and 3D models for most of their inventory, especially on specialty Chinese parts not available with Western distributors (e.g. Digikey). 

Simply select the LCSC radio button and key in the LCSC part number (that starts with a C), set your prefixes / library names and press Import!


### After adding the symbol/footprint

You should do your best to clean up the symbol and footprints after they have been imported into your library. Follow your organisations best practises, but some of the practises that we employ are:

- Double check the 3D model orientation, or import a relevant 3D model if it's not present in the ZIP file: this ensures the 3D model looks correct in the final model.
- Make sure that both the symbol and footprint has the correct prefix, which makes it easier to find specific components in the library.


### Updating this plugin

If you need to update this plugin, follow the instructions below:

1. Uninstall the plugin using the Package Content Manager (PCM)
2. Install the plugin using the new ZIP file downloaded from this repository using the PCM
3. Restart KiCad (this part is **SUPER important**! old cached files may still be present if KiCad is not restarted)


## Caveats

No known caveats yet

## Known issues

No known issues yet

## Contributing

If you encounter any issues with this repository, please do not hesitate to open an issue.
