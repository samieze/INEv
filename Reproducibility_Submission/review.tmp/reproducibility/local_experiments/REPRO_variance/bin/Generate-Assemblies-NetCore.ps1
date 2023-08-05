# Perform the code-generation step for this example application.

if ( $env:AMBVARIANTCORE ) {
    $AMBVARIANTCORE = $env:AMBVARIANTCORE
}
else {
    $AMBVARIANTCORE = "Debug\netcoreapp3.1"
}

if ( $env:AMBVARIANTCORERELEASE ) {
    $AMBVARIANTCORERELEASE = $env:AMBVARIANTCORERELEASE
}
else {
    $AMBVARIANTCORERELEASE = "Release\netcoreapp3.1"
}

if ( $env:AMBROSIATOOLS ) {
    $AMBROSIATOOLS = $env:AMBROSIATOOLS
}
else {
    $AMBROSIATOOLS = "..\..\Clients\CSharp\AmbrosiaCS\bin"
}

Write-Host "Using variant of AmbrosiaCS: $AMBVARIANTCORERELEASE"

# Generate the assemblies, assumes an .exe which is created by a .Net Framework build:
Write-Host "Executing codegen command: dotnet $AMBROSIATOOLS\$AMBVARIANTCORERELEASE\AmbrosiaCS.dll CodeGen -a=DCEP.AmbrosiaNodeAPI\bin\$AMBVARIANTCORE\DCEP.AmbrosiaNodeAPI.dll -p=DCEP.AmbrosiaNodeAPI\DCEP.AmbrosiaNodeAPI.csproj -o=DCEP.AmbrosiaNodeAPIGenerated -f=netcoreapp3.1"
& dotnet $AMBROSIATOOLS\$AMBVARIANTCORERELEASE\AmbrosiaCS.dll CodeGen -a="DCEP.AmbrosiaNodeAPI\bin\$AMBVARIANTCORE\DCEP.AmbrosiaNodeAPI.dll" -p="DCEP.AmbrosiaNodeAPI\DCEP.AmbrosiaNodeAPI.csproj" -o=DCEP.AmbrosiaNodeAPIGenerated  -f="netcoreapp3.1"
