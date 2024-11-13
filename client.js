const anchor = require('@project-serum/anchor');

const provider = anchor.AnchorProvider.local();
anchor.setProvider(provider);

const idl = JSON.parse(require('fs').readFileSync('./target/idl/mytoken.json', 'utf8'));
const programId = new anchor.web3.PublicKey('YOUR_PROGRAM_ID_HERE');
const program = new anchor.Program(idl, programId);

const mint = anchor.web3.Keypair.generate();
const tokenAccount = anchor.web3.Keypair.generate();
const user = provider.wallet.publicKey;

const totalSupply = 1000000;

async function main() {
    await program.rpc.initialize(new anchor.BN(totalSupply), {
        accounts: {
            mint: mint.publicKey,
            tokenAccount: tokenAccount.publicKey,
            user: user,
            systemProgram: anchor.web3.SystemProgram.programId,
            tokenProgram: anchor.utils.token.TOKEN_PROGRAM_ID,
            rent: anchor.web3.SYSVAR_RENT_PUBKEY,
        },
        signers: [mint, tokenAccount],
    });

    console.log('Token Minted Successfully');
}

main().catch(err => {
    console.error(err);
});

