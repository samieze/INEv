#!/bin/bash
set -euo pipefail

# Set defaults if these environment vars aren't present:
FMWK="${AMBROSIA_DOTNET_FRAMEWORK:-netcoreapp3.1}"
CONF="${AMBROSIA_DOTNET_CONF:-Release}"

if ! which AmbrosiaCS 2>/dev/null; then
    echo "ERROR: AmbrosiaCS not on PATH"
    exit 1
fi
RSRC=$(dirname `which AmbrosiaCS`)
if ! [ -d "$RSRC" ]; then
    echo "Error: directory does not exist: $RSRC"
    echo "Expected to find resource/ directory which is part of the AMBROSIA binary distribution."
    exit 1
fi

rm -rf publish

echo
echo "(STEP 1) Build enough so that we have compiled versions of our RPC interfaces"
BUILDIT="dotnet publish -o publish -c $CONF -f $FMWK "
set -x
$BUILDIT DCEP.Core/DCEP.Core.csproj /property:GenerateFullPaths=true
$BUILDIT DCEP.AmbrosiaNodeAPI/DCEP.AmbrosiaNodeAPI.csproj /property:GenerateFullPaths=true
set +x

echo
echo "(STEP 2) Use those DLL's to generate proxy code for RPC calls"

CG="AmbrosiaCS CodeGen -f netcoreapp3.1"
set -x
$CG -o DCEP.AmbrosiaNodeAPIGenerated  -a publish/DCEP.AmbrosiaNodeAPI.dll -p DCEP.AmbrosiaNodeAPI/DCEP.AmbrosiaNodeAPI.csproj
set +x

echo
echo "(STEP 3) Now the entire solution can be built."
set -x

$BUILDIT DCEP.Node/DCEP.Node.csproj /property:GenerateFullPaths=true
$BUILDIT DCEP.Simulation/DCEP.Simulation.csproj /property:GenerateFullPaths=true
$BUILDIT GeneratedSourceFiles/DCEP.AmbrosiaNodeAPIGenerated/latest/DCEP.AmbrosiaNodeAPIGenerated.csproj /property:GenerateFullPaths=true
$BUILDIT DCEP.AmbrosiaNode/DCEP.AmbrosiaNode.csproj /property:GenerateFullPaths=true

echo
echo "(STEP 4) Build linux binary."
set -x
BUILDITLINUX="dotnet publish -o publish -c $CONF -f $FMWK -r --runtime ubuntu.16.04-x64"
set +x
$BUILDIT DCEPAMBROSIA.sln
$BUILDITLINUX DCEPAMBROSIA.sln


echo
echo "(STEP 5) Copying execution scripts into bin directory and ansible scripts into publish directory."
set -x
cp scripts/*.sh publish

mkdir -p publish/bin
shopt -s extglob dotglob
mv publish/!(bin) publish/bin
shopt -u dotglob

cp ansible/* publish

mkdir -p publish/inputdata
cp -r inputexamples/* publish/inputdata



echo
echo "Project built."


