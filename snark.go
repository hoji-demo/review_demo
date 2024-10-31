package main

import (
    "crypto/sha256"
    "fmt"

    "github.com/consensys/gnark-crypto/ecc"
    "github.com/consensys/gnark/frontend"
    "github.com/consensys/gnark/frontend/cs/r1cs"
    "github.com/consensys/gnark/std/hash/sha256"
    "github.com/consensys/gnark/backend/groth16"
)

type Circuit struct {
    X frontend.Variable
    H [32]frontend.Variable `gnark:",public"`
}

func (c *Circuit) Define(api frontend.API) error {
    hash, _ := sha256.New(api)

    hash.Write(c.X)

    computedHash := hash.Sum()

    api.AssertIsEqual(computedHash[0], c.H[0])

    return nil
}

func main() {
    var circuit Circuit
    r1cs, err := frontend.Compile(ecc.BN254, r1cs.NewBuilder, &circuit)
    if err != nil {
        fmt.Println("Error compiling circuit:", err)
        return
    }

    x := 42

    h := sha256.Sum256([]byte{byte(x)})

    witness := Circuit{
        X: x,
        H: bytesToVariables(h[:]),
    }

    pk, vk, err := groth16.Setup(r1cs)
    if err != nil {
        fmt.Println("Error during setup:", err)
        return
    }

    proof, err := groth16.Prove(r1cs, pk, &witness)
    if err != nil {
        fmt.Println("Error generating proof:", err)
        return
    }

    publicInputs := Circuit{
        H: bytesToVariables(h[:]),
    }

    err = groth16.Verify(proof, vk, &publicInputs)
    if err != nil {
        fmt.Println("Proof verification failed:", err)
    } else {
        fmt.Println("Proof verification succeeded")
    }
}

func bytesToVariables(data []byte) [32]frontend.Variable {
    var vars [32]frontend.Variable
    for i := 0; i < len(data); i++ {
        vars[i] = data[i]
    }
    return vars
}

