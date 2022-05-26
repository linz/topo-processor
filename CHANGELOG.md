<a name="0.6.0"></a>
# [0.6.0](https://github.com/linz/topo-processor/compare/v0.5.0...v0.6.0) (2022-05-26)



<a name="0.5.0"></a>
# [0.5.0](https://github.com/linz/topo-processor/compare/v0.3.0...v0.5.0) (2022-05-26)


### Bug Fixes

* allow for unicode character in metadata csv ([#550](https://github.com/linz/topo-processor/issues/550)) ([0493355](https://github.com/linz/topo-processor/commit/0493355))
* aws profile and region, remove unused imports ([#585](https://github.com/linz/topo-processor/issues/585)) ([eba7f58](https://github.com/linz/topo-processor/commit/eba7f58))
* bump topo processor version in pyproject.toml ([#683](https://github.com/linz/topo-processor/issues/683)) ([89e6223](https://github.com/linz/topo-processor/commit/89e6223))
* change logs for filter_metadata and avoid looping over all metadata records while upload with survey ID ([#653](https://github.com/linz/topo-processor/issues/653)) ([2093116](https://github.com/linz/topo-processor/commit/2093116))
* ensure env vars exist ([#578](https://github.com/linz/topo-processor/issues/578)) ([c1bc714](https://github.com/linz/topo-processor/commit/c1bc714))
* force --yes ([#584](https://github.com/linz/topo-processor/issues/584)) ([ccd00c3](https://github.com/linz/topo-processor/commit/ccd00c3))
* log error for jobs that fail ([#703](https://github.com/linz/topo-processor/issues/703)) ([ed46049](https://github.com/linz/topo-processor/commit/ed46049))
* process should stop and files not transfered if any validation fails (TDE-354) ([#935](https://github.com/linz/topo-processor/issues/935)) ([7e66e47](https://github.com/linz/topo-processor/commit/7e66e47))
* remove item and collection level processing fields and extension TDE-343 ([#744](https://github.com/linz/topo-processor/issues/744)) ([6b97369](https://github.com/linz/topo-processor/commit/6b97369))
* remove metadata validator HI ([#548](https://github.com/linz/topo-processor/issues/548)) ([72af3f1](https://github.com/linz/topo-processor/commit/72af3f1))
* remove unused arguments ([#576](https://github.com/linz/topo-processor/issues/576)) ([ffb1972](https://github.com/linz/topo-processor/commit/ffb1972))
* tde-381 github action permissions ([#945](https://github.com/linz/topo-processor/issues/945)) ([8b0b350](https://github.com/linz/topo-processor/commit/8b0b350))
* update .env file and docs that reference it for SSM parameters ([#577](https://github.com/linz/topo-processor/issues/577)) ([e457c2c](https://github.com/linz/topo-processor/commit/e457c2c))
* update quality-description and collection-description ([#773](https://github.com/linz/topo-processor/issues/773)) ([e9b9f68](https://github.com/linz/topo-processor/commit/e9b9f68))
* update readme TDE-173 ([#588](https://github.com/linz/topo-processor/issues/588)) ([703d528](https://github.com/linz/topo-processor/commit/703d528))


### Features

* add correlationId to target location ([#586](https://github.com/linz/topo-processor/issues/586)) ([4cbc3f8](https://github.com/linz/topo-processor/commit/4cbc3f8))
* add quality:description ([#673](https://github.com/linz/topo-processor/issues/673)) ([d97f2b5](https://github.com/linz/topo-processor/commit/d97f2b5))
* **batch:** add geostore roles to temp buckets ([#658](https://github.com/linz/topo-processor/issues/658)) ([911034e](https://github.com/linz/topo-processor/commit/911034e))
* cache poetry dependencies so docker doesnt have to reinstall them on every build ([#565](https://github.com/linz/topo-processor/issues/565)) ([d380a46](https://github.com/linz/topo-processor/commit/d380a46))
* catch rasterio warnings to log ([#549](https://github.com/linz/topo-processor/issues/549)) ([48cc037](https://github.com/linz/topo-processor/commit/48cc037))
* **cdk:** lambda function to monitor batch job failures ([#728](https://github.com/linz/topo-processor/issues/728)) ([bbf7263](https://github.com/linz/topo-processor/commit/bbf7263))
* config for aws stacks TDE-173 ([#583](https://github.com/linz/topo-processor/issues/583)) ([daf0b04](https://github.com/linz/topo-processor/commit/daf0b04))
* create historical imagery manifest TDE-272 ([#636](https://github.com/linz/topo-processor/issues/636)) ([3430e83](https://github.com/linz/topo-processor/commit/3430e83))
* get survey files path from metadata.csv and manifest.json ([#587](https://github.com/linz/topo-processor/issues/587)) ([074c46c](https://github.com/linz/topo-processor/commit/074c46c))
* iterate all the extensions (warnings instead of raising Exception) ([#764](https://github.com/linz/topo-processor/issues/764)) ([66d588e](https://github.com/linz/topo-processor/commit/66d588e))
* iterate stac validation errors (details for each schema) ([#729](https://github.com/linz/topo-processor/issues/729)) ([119896d](https://github.com/linz/topo-processor/commit/119896d))
* load role configuration from SSM ([#563](https://github.com/linz/topo-processor/issues/563)) ([60c6500](https://github.com/linz/topo-processor/commit/60c6500))
* log loading of credentials from ssm and assuming roles ([#568](https://github.com/linz/topo-processor/issues/568)) ([63dd4ec](https://github.com/linz/topo-processor/commit/63dd4ec))
* log unique values ([#750](https://github.com/linz/topo-processor/issues/750)) ([8783f3b](https://github.com/linz/topo-processor/commit/8783f3b))
* processing:software version TDE-237 ([#680](https://github.com/linz/topo-processor/issues/680)) ([688ff9e](https://github.com/linz/topo-processor/commit/688ff9e))
* sort json keys for historical imagery TDE-338 ([#713](https://github.com/linz/topo-processor/issues/713)) ([baeec8b](https://github.com/linz/topo-processor/commit/baeec8b))
* submit script takes a source as argument (TDE-324) ([#649](https://github.com/linz/topo-processor/issues/649)) ([894b576](https://github.com/linz/topo-processor/commit/894b576))
* tde-243 validate collection ([#788](https://github.com/linz/topo-processor/issues/788)) ([0fb597c](https://github.com/linz/topo-processor/commit/0fb597c))
* update log for elastic search alert ([#698](https://github.com/linz/topo-processor/issues/698)) ([8b9ab9c](https://github.com/linz/topo-processor/commit/8b9ab9c))
* use survey name for collection title (TDE-217) ([#679](https://github.com/linz/topo-processor/issues/679)) ([c77cd24](https://github.com/linz/topo-processor/commit/c77cd24))
* use the asset encoding to determine if the asset should be decompressed ([#564](https://github.com/linz/topo-processor/issues/564)) ([3e5cbbf](https://github.com/linz/topo-processor/commit/3e5cbbf))


### Performance Improvements

* do not use rasterio to check tiff band validity TDE-333 ([#690](https://github.com/linz/topo-processor/issues/690)) ([183178e](https://github.com/linz/topo-processor/commit/183178e))



<a name="0.4.0"></a>
# [0.4.0](https://github.com/linz/topo-processor/compare/v0.3.0...v0.4.0) (2022-05-24)


### Bug Fixes

* allow for unicode character in metadata csv ([#550](https://github.com/linz/topo-processor/issues/550)) ([0493355](https://github.com/linz/topo-processor/commit/0493355))
* aws profile and region, remove unused imports ([#585](https://github.com/linz/topo-processor/issues/585)) ([eba7f58](https://github.com/linz/topo-processor/commit/eba7f58))
* bump topo processor version in pyproject.toml ([#683](https://github.com/linz/topo-processor/issues/683)) ([89e6223](https://github.com/linz/topo-processor/commit/89e6223))
* change logs for filter_metadata and avoid looping over all metadata records while upload with survey ID ([#653](https://github.com/linz/topo-processor/issues/653)) ([2093116](https://github.com/linz/topo-processor/commit/2093116))
* ensure env vars exist ([#578](https://github.com/linz/topo-processor/issues/578)) ([c1bc714](https://github.com/linz/topo-processor/commit/c1bc714))
* force --yes ([#584](https://github.com/linz/topo-processor/issues/584)) ([ccd00c3](https://github.com/linz/topo-processor/commit/ccd00c3))
* log error for jobs that fail ([#703](https://github.com/linz/topo-processor/issues/703)) ([ed46049](https://github.com/linz/topo-processor/commit/ed46049))
* process should stop and files not transfered if any validation fails (TDE-354) ([#935](https://github.com/linz/topo-processor/issues/935)) ([7e66e47](https://github.com/linz/topo-processor/commit/7e66e47))
* remove item and collection level processing fields and extension TDE-343 ([#744](https://github.com/linz/topo-processor/issues/744)) ([6b97369](https://github.com/linz/topo-processor/commit/6b97369))
* remove metadata validator HI ([#548](https://github.com/linz/topo-processor/issues/548)) ([72af3f1](https://github.com/linz/topo-processor/commit/72af3f1))
* remove unused arguments ([#576](https://github.com/linz/topo-processor/issues/576)) ([ffb1972](https://github.com/linz/topo-processor/commit/ffb1972))
* update .env file and docs that reference it for SSM parameters ([#577](https://github.com/linz/topo-processor/issues/577)) ([e457c2c](https://github.com/linz/topo-processor/commit/e457c2c))
* update quality-description and collection-description ([#773](https://github.com/linz/topo-processor/issues/773)) ([e9b9f68](https://github.com/linz/topo-processor/commit/e9b9f68))
* update readme TDE-173 ([#588](https://github.com/linz/topo-processor/issues/588)) ([703d528](https://github.com/linz/topo-processor/commit/703d528))


### Features

* add correlationId to target location ([#586](https://github.com/linz/topo-processor/issues/586)) ([4cbc3f8](https://github.com/linz/topo-processor/commit/4cbc3f8))
* add quality:description ([#673](https://github.com/linz/topo-processor/issues/673)) ([d97f2b5](https://github.com/linz/topo-processor/commit/d97f2b5))
* **batch:** add geostore roles to temp buckets ([#658](https://github.com/linz/topo-processor/issues/658)) ([911034e](https://github.com/linz/topo-processor/commit/911034e))
* cache poetry dependencies so docker doesnt have to reinstall them on every build ([#565](https://github.com/linz/topo-processor/issues/565)) ([d380a46](https://github.com/linz/topo-processor/commit/d380a46))
* catch rasterio warnings to log ([#549](https://github.com/linz/topo-processor/issues/549)) ([48cc037](https://github.com/linz/topo-processor/commit/48cc037))
* **cdk:** lambda function to monitor batch job failures ([#728](https://github.com/linz/topo-processor/issues/728)) ([bbf7263](https://github.com/linz/topo-processor/commit/bbf7263))
* config for aws stacks TDE-173 ([#583](https://github.com/linz/topo-processor/issues/583)) ([daf0b04](https://github.com/linz/topo-processor/commit/daf0b04))
* create historical imagery manifest TDE-272 ([#636](https://github.com/linz/topo-processor/issues/636)) ([3430e83](https://github.com/linz/topo-processor/commit/3430e83))
* get survey files path from metadata.csv and manifest.json ([#587](https://github.com/linz/topo-processor/issues/587)) ([074c46c](https://github.com/linz/topo-processor/commit/074c46c))
* iterate all the extensions (warnings instead of raising Exception) ([#764](https://github.com/linz/topo-processor/issues/764)) ([66d588e](https://github.com/linz/topo-processor/commit/66d588e))
* iterate stac validation errors (details for each schema) ([#729](https://github.com/linz/topo-processor/issues/729)) ([119896d](https://github.com/linz/topo-processor/commit/119896d))
* load role configuration from SSM ([#563](https://github.com/linz/topo-processor/issues/563)) ([60c6500](https://github.com/linz/topo-processor/commit/60c6500))
* log loading of credentials from ssm and assuming roles ([#568](https://github.com/linz/topo-processor/issues/568)) ([63dd4ec](https://github.com/linz/topo-processor/commit/63dd4ec))
* log unique values ([#750](https://github.com/linz/topo-processor/issues/750)) ([8783f3b](https://github.com/linz/topo-processor/commit/8783f3b))
* processing:software version TDE-237 ([#680](https://github.com/linz/topo-processor/issues/680)) ([688ff9e](https://github.com/linz/topo-processor/commit/688ff9e))
* sort json keys for historical imagery TDE-338 ([#713](https://github.com/linz/topo-processor/issues/713)) ([baeec8b](https://github.com/linz/topo-processor/commit/baeec8b))
* submit script takes a source as argument (TDE-324) ([#649](https://github.com/linz/topo-processor/issues/649)) ([894b576](https://github.com/linz/topo-processor/commit/894b576))
* tde-243 validate collection ([#788](https://github.com/linz/topo-processor/issues/788)) ([0fb597c](https://github.com/linz/topo-processor/commit/0fb597c))
* update log for elastic search alert ([#698](https://github.com/linz/topo-processor/issues/698)) ([8b9ab9c](https://github.com/linz/topo-processor/commit/8b9ab9c))
* use survey name for collection title (TDE-217) ([#679](https://github.com/linz/topo-processor/issues/679)) ([c77cd24](https://github.com/linz/topo-processor/commit/c77cd24))
* use the asset encoding to determine if the asset should be decompressed ([#564](https://github.com/linz/topo-processor/issues/564)) ([3e5cbbf](https://github.com/linz/topo-processor/commit/3e5cbbf))


### Performance Improvements

* do not use rasterio to check tiff band validity TDE-333 ([#690](https://github.com/linz/topo-processor/issues/690)) ([183178e](https://github.com/linz/topo-processor/commit/183178e))



# [0.3.0](https://github.com/linz/topo-processor/compare/v0.2.0...v0.3.0) (2022-02-02)


### Features

* **ci:** create github releases in ci ([#544](https://github.com/linz/topo-processor/issues/544)) ([74ceb4c](https://github.com/linz/topo-processor/commit/74ceb4c941ef1bcb4283f8ded9cbc4fb6777930b))



# 0.2.0 (2022-02-02)


### Bug Fixes

* add missing typing for [no-any-return] (TDE-267)  ([#507](https://github.com/linz/topo-processor/issues/507)) ([c490b94](https://github.com/linz/topo-processor/commit/c490b940a70408e6b84d68e58783152fde97da1f))
* add missing typing for function arguments [arg-type] (TDE-263) ([#502](https://github.com/linz/topo-processor/issues/502)) ([d4b6c46](https://github.com/linz/topo-processor/commit/d4b6c462cffa16ce123a4ff6e917138750635ade))
* add missing typing for type arguments [type-arg] (TDE-266) ([#505](https://github.com/linz/topo-processor/issues/505)) ([a97b77f](https://github.com/linz/topo-processor/commit/a97b77f144d3068f3773ae935288cf5c3aa3fe5a))
* asset object key redo (TDE-188) ([#434](https://github.com/linz/topo-processor/issues/434)) ([6529505](https://github.com/linz/topo-processor/commit/6529505d4ebb1423200724b6f54b7e734b5e8f84))
* bytes need to be decoded first ([#411](https://github.com/linz/topo-processor/issues/411)) ([82c096e](https://github.com/linz/topo-processor/commit/82c096e030eae38429ec1a4287ed29f46667e845))
* centroid has to be an int or a float (TDE-286) ([#526](https://github.com/linz/topo-processor/issues/526)) ([29f6988](https://github.com/linz/topo-processor/commit/29f69888f1ff900abe643e1581e0f5aafb06d9fb))
* circular imports ([#363](https://github.com/linz/topo-processor/issues/363)) ([31ec0b2](https://github.com/linz/topo-processor/commit/31ec0b2115ef3a3b82241bfba1c9e0472cf81c0f))
* cleanup ([#397](https://github.com/linz/topo-processor/issues/397)) ([7b84991](https://github.com/linz/topo-processor/commit/7b84991ced19809229569aaae0b8dca15503de10))
* convert scanned date to UTC (TDE-187) ([#406](https://github.com/linz/topo-processor/issues/406)) ([357ce63](https://github.com/linz/topo-processor/commit/357ce631e115e13aaef30f3f13f4ee8328ddd780))
* correct abstract method signature to comply with [override] (TDE-280] ([#516](https://github.com/linz/topo-processor/issues/516)) ([77759a2](https://github.com/linz/topo-processor/commit/77759a2ac8fdfe7e863514912f88b256eec91265))
* correct imports to comply with [attr-defined] (TDE-269) ([#511](https://github.com/linz/topo-processor/issues/511)) ([3cc6b90](https://github.com/linz/topo-processor/commit/3cc6b9084e1783efbca1d9d4f29737110c3c788c))
* correct issue with union attribute typing [union-attr] (TDE-268) ([#508](https://github.com/linz/topo-processor/issues/508)) ([d12340c](https://github.com/linz/topo-processor/commit/d12340c2159545b0bd0195319423a5c7e255514d))
* improve test data names ([#177](https://github.com/linz/topo-processor/issues/177)) ([5c3c373](https://github.com/linz/topo-processor/commit/5c3c37349e80f11d200a4e68ca6629c38ea93269))
* item compatible with the list type [list-item] (TDE-282) ([#519](https://github.com/linz/topo-processor/issues/519)) ([1450175](https://github.com/linz/topo-processor/commit/14501759331c33eba8662a24e18e08c4d212461d))
* **metadata-loaders:** include required eo and proj metadata in the historical imagery metadata loader ([#424](https://github.com/linz/topo-processor/issues/424)) (TDE-213) ([d697aa5](https://github.com/linz/topo-processor/commit/d697aa5e08bd24fcdb977f84c935367a783876f6))
* mypy [no-untyped-def] typing (TDE-264) ([#509](https://github.com/linz/topo-processor/issues/509)) ([9143a4b](https://github.com/linz/topo-processor/commit/9143a4b12cb10dd64e8282e02985e774681e58b8))
* mypy assignment (TDE-277) ([#513](https://github.com/linz/topo-processor/issues/513)) ([f3c0467](https://github.com/linz/topo-processor/commit/f3c046756236c5b72e37f9353541b337d49b6b57))
* non tiff files can also be uploaded ([#163](https://github.com/linz/topo-processor/issues/163)) ([5053b8d](https://github.com/linz/topo-processor/commit/5053b8d377f2cd32163933cdcdbd783e9570457e))
* not overwriting json files and added more test data ([#75](https://github.com/linz/topo-processor/issues/75)) ([e082df3](https://github.com/linz/topo-processor/commit/e082df3d36323de4653bcbd5e6b5b462a841ebee))
* only process tiff files for historical imagery ([#421](https://github.com/linz/topo-processor/issues/421)) ([edba3c1](https://github.com/linz/topo-processor/commit/edba3c1abab8aa5b71c6e0aade323375bbe9ed88))
* populate stac metadata hrefs with relative links ([#276](https://github.com/linz/topo-processor/issues/276)) ([8f2dfc1](https://github.com/linz/topo-processor/commit/8f2dfc1d2a38dad75e956c088801f7ebf43f0cf8))
* recursive file scanning ([#277](https://github.com/linz/topo-processor/issues/277)) ([f01542c](https://github.com/linz/topo-processor/commit/f01542ceec2c479bc723eb4a270518ca45e956a0))
* remove use of Any in an Union (TDE-278) ([#512](https://github.com/linz/topo-processor/issues/512)) ([a94d060](https://github.com/linz/topo-processor/commit/a94d06042918d17b259993a15deb99110e6240e2))
* return types ([#510](https://github.com/linz/topo-processor/issues/510)) ([2931ae9](https://github.com/linz/topo-processor/commit/2931ae9679db0fd2ad7d21d40f55338728df8276))
* speed up csv extractor ([#86](https://github.com/linz/topo-processor/issues/86)) ([a881f22](https://github.com/linz/topo-processor/commit/a881f223bd16b910cb78b4ad59947bae8454a8ae))
* type annotate some variables ([#524](https://github.com/linz/topo-processor/issues/524)) ([d9992b4](https://github.com/linz/topo-processor/commit/d9992b4b8fdfa2df0e133ffebb8772092c908c58))
* typing annotation None to Generator for pytest setup functions (TDE-285) ([#525](https://github.com/linz/topo-processor/issues/525)) ([51ca5da](https://github.com/linz/topo-processor/commit/51ca5da6daa9796005ff86d4ee8ab320e9a4794d))
* update pystac to v.1.1.0 ([#345](https://github.com/linz/topo-processor/issues/345)) ([debdb4b](https://github.com/linz/topo-processor/commit/debdb4b082b2d1d5741d1a61c0b3d9aa0f538481))
* use continue to stop code from exiting loop ([#239](https://github.com/linz/topo-processor/issues/239)) ([24fbbde](https://github.com/linz/topo-processor/commit/24fbbde261a89f464d6e07bfb651e5600ebc5879))
* use https://spdx.org/licenses/ CC-BY-4.0 ([#288](https://github.com/linz/topo-processor/issues/288)) ([0fc4566](https://github.com/linz/topo-processor/commit/0fc45663f133facf426d9cd62931f920eabfdad0))
* **validate:** convert tuple into array to work around jsonschema-rs validation crash on tuple type (TDE-186) ([#404](https://github.com/linz/topo-processor/issues/404)) ([41a898b](https://github.com/linz/topo-processor/commit/41a898b8231a99bbb437ed30595886ba974f989e))
* **validate:** validate STAC Item against item-spec json schema (TDE-204) ([#405](https://github.com/linz/topo-processor/issues/405)) ([df654de](https://github.com/linz/topo-processor/commit/df654deaed58329bd8ba6ba3d518aff41544f9be))
* variable values type [type-var] (TDE-281) ([#518](https://github.com/linz/topo-processor/issues/518)) ([52d3336](https://github.com/linz/topo-processor/commit/52d3336c78a468cc4646d52b2eaf33b54c57f8ef))


### Features

* add aerial photo stac extension ([#383](https://github.com/linz/topo-processor/issues/383)) ([76778a8](https://github.com/linz/topo-processor/commit/76778a84455887142f4b9825f3a88e59203fe582))
* add gdal_translate options (TDE-80) (TDE-260) ([#503](https://github.com/linz/topo-processor/issues/503)) ([4f6a121](https://github.com/linz/topo-processor/commit/4f6a121dfd8a7d67acb5b8526ee2b3e4b46fa935)), closes [#472](https://github.com/linz/topo-processor/issues/472)
* add scanning stac extension ([#385](https://github.com/linz/topo-processor/issues/385)) ([a231380](https://github.com/linz/topo-processor/commit/a2313807d4b4e6d4bad4ac52b46de5b2db37a290))
* add trace log ([#193](https://github.com/linz/topo-processor/issues/193)) ([3d67baa](https://github.com/linz/topo-processor/commit/3d67baaeb4711f7ed85ba32dbb9b50a37c1d1a8d))
* added logging for item and collection ([#72](https://github.com/linz/topo-processor/issues/72)) ([f3092a8](https://github.com/linz/topo-processor/commit/f3092a8c560f2805eff122b4f7a01751e4fe2913))
* added subprocess and tests ([#113](https://github.com/linz/topo-processor/issues/113)) ([bffaaf3](https://github.com/linz/topo-processor/commit/bffaaf39a3705bb30456865481972d7d3941d0c5))
* added the ability to create cog ([#114](https://github.com/linz/topo-processor/issues/114)) ([888f809](https://github.com/linz/topo-processor/commit/888f80912dd240e3e25e61a799c810fefa527720))
* AWS CDK infrastructure (TDE-219) ([#534](https://github.com/linz/topo-processor/issues/534)) ([39a8ed3](https://github.com/linz/topo-processor/commit/39a8ed3d47b584e0367ce395dd979989b7c7c0db))
* cli to upload data to s3 ([#112](https://github.com/linz/topo-processor/issues/112)) ([5d690c8](https://github.com/linz/topo-processor/commit/5d690c822daca580a68217ba4727a091e7d6ef6f))
* cog from s3 ([#224](https://github.com/linz/topo-processor/issues/224)) ([f0e1859](https://github.com/linz/topo-processor/commit/f0e185991b559d91b718305fa4e4d4f187ca5fe7))
* **cog:** add arguments for lossless tiff compression ([#471](https://github.com/linz/topo-processor/issues/471)) ([2851a3d](https://github.com/linz/topo-processor/commit/2851a3df6df04ea3fdb5f9c5eab46d1fd7cba246))
* create bounding boxes/polygons from wkt ([#389](https://github.com/linz/topo-processor/issues/389)) ([e96346f](https://github.com/linz/topo-processor/commit/e96346f7fdd93ca94f11cfd6da99390880b55ded))
* create collection store  ([#147](https://github.com/linz/topo-processor/issues/147)) ([53f3990](https://github.com/linz/topo-processor/commit/53f3990bcc71fde041765f71b50da4b50ae5ef14))
* create Dockerfile ([#521](https://github.com/linz/topo-processor/issues/521)) ([6c46a46](https://github.com/linz/topo-processor/commit/6c46a468a0cf9f9845ad86b71d44ae1a6682da54))
* created collection and item creators ([#55](https://github.com/linz/topo-processor/issues/55)) ([f71427f](https://github.com/linz/topo-processor/commit/f71427f82842f1a03a981a9448ff62d84d577837))
* created internal rep of item and asset for local upload ([#140](https://github.com/linz/topo-processor/issues/140)) ([34956d7](https://github.com/linz/topo-processor/commit/34956d7199e75de92abeeb4dad094654e9345ff6))
* extract more metadata from tiff ([#84](https://github.com/linz/topo-processor/issues/84)) ([fbbba95](https://github.com/linz/topo-processor/commit/fbbba95376b8eefc9d22cf2fcbd5725049f48887))
* handle multiple assets with transformations ([#145](https://github.com/linz/topo-processor/issues/145)) ([d37f025](https://github.com/linz/topo-processor/commit/d37f0259d1139a95a0974aefa267e65eb46afc21))
* hash data after data transformation ([#133](https://github.com/linz/topo-processor/issues/133)) ([76dc0d5](https://github.com/linz/topo-processor/commit/76dc0d54545dca0356d1d56711b3c2972209f4c1))
* implement historical imagery stac extension ([#402](https://github.com/linz/topo-processor/issues/402)) ([3b2c726](https://github.com/linz/topo-processor/commit/3b2c72659c7f9997bcd924f32f87916cd5957891))
* implement providers ([#420](https://github.com/linz/topo-processor/issues/420)) ([3ad50d5](https://github.com/linz/topo-processor/commit/3ad50d5380b6030b9c582ddff50cf70841b0621d))
* implement summaries ([#469](https://github.com/linz/topo-processor/issues/469)) ([56c5b16](https://github.com/linz/topo-processor/commit/56c5b16ba8f043f3aa04dacefdac24e727feb58f))
* integrate mypy library for type checking (TDE-183) ([#392](https://github.com/linz/topo-processor/issues/392)) ([3e61ea9](https://github.com/linz/topo-processor/commit/3e61ea9d38889006f55ce890ffb9bb829b000081))
* link collection and item stac objects ([#153](https://github.com/linz/topo-processor/issues/153)) ([3cf2b8b](https://github.com/linz/topo-processor/commit/3cf2b8bbd094afb13c18707717cd2132b3d83b74))
* multihash-implementation ([#80](https://github.com/linz/topo-processor/issues/80)) ([6c04a63](https://github.com/linz/topo-processor/commit/6c04a637a41f4f2e3bdace8ffceefaec1155ec03))
* only cog historical imagery ([#119](https://github.com/linz/topo-processor/issues/119)) ([86324f4](https://github.com/linz/topo-processor/commit/86324f41cf760cbda67a05fb896af8ac1dd78c41))
* only write valid item ([#151](https://github.com/linz/topo-processor/issues/151)) ([7f44456](https://github.com/linz/topo-processor/commit/7f44456773aad935057cf49891297a0f92430b11))
* read from and write to both s3 and local ([#213](https://github.com/linz/topo-processor/issues/213)) ([eb03814](https://github.com/linz/topo-processor/commit/eb0381445b1e0e953718686f486406646873229b))
* README ([#360](https://github.com/linz/topo-processor/issues/360)) ([2de886a](https://github.com/linz/topo-processor/commit/2de886a71593d2ff7368d37111bbdacbaa69885a))
* set temporal extent (TDE-148) ([#393](https://github.com/linz/topo-processor/issues/393)) ([1e4b717](https://github.com/linz/topo-processor/commit/1e4b717bb6f929c5c38cdbfd18802778da65f668))
* update extension urls to stac.linz.govt.nz ([#439](https://github.com/linz/topo-processor/issues/439)) ([48dc37e](https://github.com/linz/topo-processor/commit/48dc37eb708ef4b83b1f9c8be4e4718d413c1914))
* **upload:** use LDS Cache ([#454](https://github.com/linz/topo-processor/issues/454)) (TDE-176) ([0c0afb1](https://github.com/linz/topo-processor/commit/0c0afb1b13adf5b96475e6711f23320e502e4866))
* use camera extension ([#353](https://github.com/linz/topo-processor/issues/353)) ([365a443](https://github.com/linz/topo-processor/commit/365a44359f97c5e6c16377ad5bc3e1ca35ee0e62))
* use linz stac schema TDE-156 ([#452](https://github.com/linz/topo-processor/issues/452)) ([4f3c81d](https://github.com/linz/topo-processor/commit/4f3c81d0ee53292f7cafba7ddfcc3c8ca01fc907))
* **use-film-extension:** TDE-162 ([#380](https://github.com/linz/topo-processor/issues/380)) ([78c8fe1](https://github.com/linz/topo-processor/commit/78c8fe1fb04004e096cdeb797b7a9d7ae131456d))
* **validate:** support LDS cache of Historical Imagery metadata as source (TDE-202) ([#448](https://github.com/linz/topo-processor/issues/448)) ([3059e54](https://github.com/linz/topo-processor/commit/3059e54e3262bf1df7f1056c1fcaab10e3f3eda8))
* **validate:** validate STAC Collection (TDE-170) ([#416](https://github.com/linz/topo-processor/issues/416)) ([19a8c1a](https://github.com/linz/topo-processor/commit/19a8c1adcb626dbcb583c48029f9e446973a17ba))
* **validate:** validation against local schema for tests (TDE-234) ([#443](https://github.com/linz/topo-processor/issues/443)) ([3be696d](https://github.com/linz/topo-processor/commit/3be696dcbcc6be704d05eb3b20d893fc7414ae55))


### Performance Improvements

* fast metadata validation (TDE-181) ([#391](https://github.com/linz/topo-processor/issues/391)) ([5869d8e](https://github.com/linz/topo-processor/commit/5869d8e95fa3b045fa19660623ebf24a8a934a15))
* integration test (TDE-191) ([#427](https://github.com/linz/topo-processor/issues/427)) ([48c5032](https://github.com/linz/topo-processor/commit/48c5032fb2559375c79066b5b11d1e4ab52cc80a))
* json loads/dumps is no longer needed as tuples are handled by jsonschema_rs ([#412](https://github.com/linz/topo-processor/issues/412)) ([19f759b](https://github.com/linz/topo-processor/commit/19f759bdd3e9b0773544946af273d474c5916159))



