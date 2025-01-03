from typing import Union

from loguru import logger

from src.client import Client
from src.utils import Utils
from src.vars import ERC721_ABI, ERC721_BYTECODE


class ERC721Manager:
    async def deploy_erc721(self, client_ink: Client, name: str, symbol: str, account_index: int, is_first_tx: bool = False) -> Union[bool, str]:
        balance = await client_ink.w3.eth.get_balance(client_ink.wallet_address)
        
        if balance <= 0:
            logger.error(f'Account {account_index+1} | {client_ink.wallet_address} | Deploy cancelled: zero balance.')
            return False
        
        try:
            logger.info(f'Account {account_index+1} | {client_ink.wallet_address} | Attempting to deploy ERC-721 contract in {client_ink.network.name}...')
            if is_first_tx:
                result = await client_ink.deploy_contract(
                    name=name,
                    symbol=symbol,
                    abi_path=ERC721_ABI,
                    bytecode_path=ERC721_BYTECODE
                )
            else:
                result = await Utils.execute_with_delay(client_ink.deploy_contract(
                    name=name,
                    symbol=symbol,
                    abi_path=ERC721_ABI,
                    bytecode_path=ERC721_BYTECODE
                ), client_ink.wallet_address, account_index)
            
            return result
        except Exception as e:
            logger.error(f'Account {account_index+1} | {client_ink.wallet_address} | Error during deploying ERC-721 contract: {e}.')
            return False

    async def mint_nft(self, client_ink: Client, contract_address: str, account_index: int) -> bool:
        balance = await client_ink.w3.eth.get_balance(client_ink.wallet_address)
        
        if balance <= 0:
            logger.error(f'Account {account_index+1} | {client_ink.wallet_address} | Mint cancelled: zero balance.')
            return False
        
        try:
            logger.info(f'Account {account_index+1} | {client_ink.wallet_address} | Attempting to mint NFT with contract {contract_address}...')
            result = await Utils.execute_with_delay(client_ink.mint_nft(
                contract_address=contract_address, 
                abi_path=ERC721_ABI
            ), client_ink.wallet_address, account_index)
            
            return result
        except Exception as e:
            logger.error(f'Account {account_index+1} | {client_ink.wallet_address} | Error during minting NFT: {e}.')
            return False
