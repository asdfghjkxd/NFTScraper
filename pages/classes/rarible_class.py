import os
import pickle
import pandas as pd
import json

from typing import Optional
from utils.utils import assertType


class Rarible:
    def __init__(self):
        self.none_type = type(None)
        self.ownershipId_type = str
        self.contract_type = str
        self.tokenId_type = int
        self.continuation_type = (str, self.none_type)
        self.size_type = (str, self.none_type)
        self.itemId_type = str
        self.includeMeta_type = (bool, self.none_type)
        self.owner_type = str
        self.creator_type = str
        self.collection_type = str
        self.showDeleted_type = [bool, self.none_type]
        self.lastUpdatedFrom_type = [int, self.none_type]
        self.lastUpdatedTo_type = [int, self.none_type]
        self.minter_type = str
        self.type_type = str
        self.type_conditions = ['TRANSFER_FROM', 'TRANSFER_TO', 'MINT', 'BURN', 'MAKE_BID', 'GET_BID', 'LIST', 'BUY',
                                'SELL']
        self.user_type = str

        self.URLs = []


class Ownership(Rarible):
    def __init__(self):
        super().__init__()

    def setNFTByIDParameter(self,
                            ownershipId: str):
        """
        Get and set parameters for for querying NFT ownership by Ownership ID

        :param ownershipId:                         Ownership ID
        """

        if assertType(self.ownershipId_type, ownershipId):
            if ownershipId is not None:
                self.endpoint = f'https://api-staging.rarible.com/protocol/v0.1/ethereum/nft/ownerships/{ownershipId}'
                self.URLs.append(self.endpoint)

    def setNFTByItemParameter(self,
                              contract: str,
                              tokenId: int,
                              continuation: Optional[str],
                              size: int):
        """
        Get and set parameters for querying NFT ownership by Item ID

        :param contract:                            Contract Address
        :param tokenId:                             Token ID (int)
        :param continuation:                        Continuation String
        :param size:                                Size
        """

        temp = ''
        param = {}
        self.endpoint = 'https://api-staging.rarible.com/protocol/v0.1/ethereum/nft/ownerships/byItem'

        if assertType(self.contract_type, contract):
            if contract is not None:
                param['contract'] = contract

        if assertType(self.tokenId_type, tokenId):
            if tokenId is not None:
                param['tokenId'] = tokenId

        if assertType(self.continuation_type, continuation):
            if continuation is not None:
                param['continuation'] = continuation

        if assertType(self.size_type, size):
            if size is not None:
                param['size'] = size

        for counter, (key, value) in enumerate(param.items()):
            if counter == 0:
                temp = temp + f'?{key}={value}'
            elif counter > 0:
                temp = temp + f'&{key}={value}'

        self.URLs.append(f'{self.endpoint}{temp}')

    def setNFTAllParameter(self,
                           continuation: str,
                           size: int):
        """
        Get and set parameters for querying all NFT ownership

        :param continuation:                        Continuation String
        :param size:                                Size
        """

        temp = ''
        param = {}
        self.endpoint = 'https://api-staging.rarible.com/protocol/v0.1/ethereum/nft/ownerships/all'

        if assertType(self.continuation_type, continuation):
            if continuation is not None:
                param['continuation'] = continuation

        if assertType(self.size_type, size):
            if size is not None:
                param['size'] = size

        for counter, (key, value) in enumerate(param.items()):
            if counter == 0:
                temp = temp + f'?{key}={value}'
            elif counter > 0:
                temp = temp + f'&{key}={value}'

        self.URLs.append(f'{self.endpoint}{temp}')

    def parseNFTByIDParameter(self):
        pass

    def parseNFTByItemParameter(self):
        pass

    def parseNFTAllParameter(self):
        pass


class Item(Rarible):
    def __init__(self):
        super().__init__()

    def setNFTMetaByID(self,
                       itemId: str):
        """
        Gets and sets parameters for querying NFT metadata by Item ID

        :param itemId:                              Item ID
        """

        self.endpoint = 'https://api-staging.rarible.com/protocol/v0.1/ethereum/nft/items/'

        if assertType(self.itemId_type, itemId):
            if itemId is not None:
                self.URLs.append(f'{self.endpoint}{itemId}/meta')

    def setNFTLazyItemByID(self,
                           itemId: str):
        """
        Gets and sets parameters for lazy querying NFT by Item ID

        :param itemId:                              Item ID
        """

        self.endpoint = 'https://api-staging.rarible.com/protocol/v0.1/ethereum/nft/items/'

        if assertType(self.itemId_type, itemId):
            if itemId is not None:
                self.URLs.append(f'{self.endpoint}{itemId}/lazy')

    def setNFTItemByID(self,
                       itemId: str,
                       includeMeta: Optional[bool]):
        """
        Gets and sets parameters for querying NFT by Item ID

        :param itemId:                              Item ID
        :param includeMeta:                         Include Metadata for NFT in response
        """

        self.endpoint = 'https://api-staging.rarible.com/protocol/v0.1/ethereum/nft/items/'

        if assertType(self.itemId_type, itemId):
            if itemId is not None:
                self.endpoint = f'{self.endpoint}{itemId}'

        if assertType(self.includeMeta_type, includeMeta):
            if includeMeta is not None:
                self.endpoint = f'{self.endpoint}?includeMeta={str(includeMeta).lower()}'

        self.URLs.append(self.endpoint)

    def setNFTItemByOwner(self,
                          owner: str,
                          continuation: Optional[str],
                          size: Optional[int],
                          includeMeta: Optional[bool]):
        """
        Gets and sets parameters for querying NFT by owner

        :param owner:                               Owner
        :param continuation:                        Continuation String
        :param size:                                Size
        :param includeMeta:                         Include Metadata for NFT in response
        """

        temp = ''
        param = {}

        self.endpoint = 'https://api-staging.rarible.com/protocol/v0.1/ethereum/nft/items/byOwner'

        if assertType(self.owner_type, owner):
            if owner is not None:
                param['owner'] = owner

        if assertType(self.itemId_type, continuation):
            if continuation is not None:
                param['continuation'] = continuation

        if assertType(self.size_type, size):
            if size is not None:
                param['size'] = size

        if assertType(self.includeMeta_type, includeMeta):
            if includeMeta is not None:
                param['includeMeta'] = includeMeta

        for counter, (key, value) in enumerate(param.items()):
            if counter == 0:
                temp = temp + f'?{key}={value}'
            elif counter > 0:
                temp = temp + f'&{key}={value}'

        self.URLs.append(f'{self.endpoint}{temp}')

    def setNFTItemByCreator(self,
                            creator: str,
                            continuation: Optional[str],
                            size: Optional[int],
                            includeMeta: Optional[bool]):
        """
        Gets and sets parameters for querying NFT by creator

        :param creator:                             Creator name
        :param continuation:                        Continuation String
        :param size:                                Size
        :param includeMeta:                         Include Metadata for NFT in response
        """

        temp = ''
        param = {}

        self.endpoint = 'https://api-staging.rarible.com/protocol/v0.1/ethereum/nft/items/byCreator'

        if assertType(self.creator_type, creator):
            if creator is not None:
                param['creator'] = creator

        if assertType(self.itemId_type, continuation):
            if continuation is not None:
                param['continuation'] = continuation

        if assertType(self.size_type, size):
            if size is not None:
                param['size'] = size

        if assertType(self.includeMeta_type, includeMeta):
            if includeMeta is not None:
                param['includeMeta'] = includeMeta

        for counter, (key, value) in enumerate(param.items()):
            if counter == 0:
                temp = temp + f'?{key}={value}'
            elif counter > 0:
                temp = temp + f'&{key}={value}'

        self.URLs.append(f'{self.endpoint}{temp}')

    def setNFTItemByCollection(self,
                               collection: str,
                               continuation: Optional[str],
                               size: Optional[int],
                               includeMeta: Optional[bool]):
        """
        Gets and sets parameters for querying NFT by collection

        :param collection:                          Collection
        :param continuation:                        Continuation String
        :param size:                                Size
        :param includeMeta:                         Include Metadata for NFT in response
        """

        temp = ''
        param = {}

        self.endpoint = 'https://api-staging.rarible.com/protocol/v0.1/ethereum/nft/items/byCollection'

        if assertType(self.collection_type, collection):
            if collection is not None:
                param['collection'] = collection

        if assertType(self.itemId_type, continuation):
            if continuation is not None:
                param['continuation'] = continuation

        if assertType(self.size_type, size):
            if size is not None:
                param['size'] = size

        if assertType(self.includeMeta_type, includeMeta):
            if includeMeta is not None:
                param['includeMeta'] = includeMeta

        for counter, (key, value) in enumerate(param.items()):
            if counter == 0:
                temp = temp + f'?{key}={value}'
            elif counter > 0:
                temp = temp + f'&{key}={value}'

        self.URLs.append(f'{self.endpoint}{temp}')

    def setNFTAllItems(self,
                       continuation: Optional[str],
                       size: Optional[int],
                       showDeleted: Optional[bool],
                       lastUpdatedFrom: Optional[int],
                       lastUpdatedTo: Optional[int],
                       includeMeta: Optional[bool]):
        """
        Gets and sets parameters for querying all NFT

        :param continuation:                        Continuation String
        :param size:                                Size
        :param showDeleted:                         Show Deleted
        :param lastUpdatedFrom:                     Last Updated Form
        :param lastUpdatedTo:                       Last Updated To
        :param includeMeta:                         Include Metadata for NFT in response
        """

        temp = ''
        param = {}
        self.endpoint = 'https://api-staging.rarible.com/protocol/v0.1/ethereum/nft/items/all'

        if assertType(self.continuation_type, continuation):
            if continuation is not None:
                param['continuation'] = continuation

        if assertType(self.size_type, size):
            if size is not None:
                param['size'] = size

        if assertType(self.showDeleted_type, showDeleted):
            if showDeleted is not None:
                param['showDeleted'] = showDeleted

        if assertType(self.lastUpdatedFrom_type, lastUpdatedFrom):
            if lastUpdatedFrom is not None:
                param['lastUpdatedFrom'] = lastUpdatedFrom

        if assertType(self.lastUpdatedTo_type, lastUpdatedTo):
            if lastUpdatedTo is not None:
                param['lastUpdatedTo'] = lastUpdatedTo

        if assertType(self.includeMeta_type, includeMeta):
            if includeMeta is not None:
                param['includeMeta'] = includeMeta

        for counter, (key, value) in enumerate(param.items()):
            if counter == 0:
                temp = temp + f'?{key}={value}'
            elif counter > 0:
                temp = temp + f'&{key}={value}'

        self.URLs.append(f'{self.endpoint}{temp}')

    def parseNFTMetaByID(self):
        pass

    def parseNFTLazyItemByID(self):
        pass

    def parseNFTItemByID(self):
        pass

    def parseNFTItemByOwner(self):
        pass

    def parseNFTItemByCreator(self):
        pass

    def parseNFTItemByCollection(self):
        pass

    def parseNFTAllItems(self):
        pass


class Collection(Rarible):
    def __init__(self):
        super().__init__()

    def setGenerateNFTID(self,
                         collection: str,
                         minter: str):
        """
        Gets and sets the parameters needed to query for the next available tokenId for minter

        :param collection:                          Address of Collection
        :param minter:                              Minter Address
        """

        self.endpoint = 'https://api-staging.rarible.com/protocol/v0.1/ethereum/nft/collections/'

        if assertType(self.collection_type, collection):
            if collection is not None:
                self.endpoint = f'{self.endpoint}{collection}/generate_token_id'

        if assertType(self.minter_type, minter):
            if minter is not None:
                self.endpoint = f'{self.endpoint}?minter={minter}'

        self.URLs.append(self.endpoint)

    def setNFTCollectionByID(self,
                             collection: str):
        """
        Gets and sets the parameters needed for querying a collection by ID
        :param collection:                          Address of Collection
        """

        self.endpoint = 'https://api-staging.rarible.com/protocol/v0.1/ethereum/nft/collections/'

        if assertType(self.collection_type, collection):
            if collection is not None:
                self.endpoint = f'{self.endpoint}{collection}'

        self.URLs.append(self.endpoint)

    def setQueryCollectionsByOwner(self,
                                   owner: str,
                                   continuation: Optional[str],
                                   size: Optional[int]):
        """
        Gets and sets the parameters needed for querying collections by owner

        :param owner:                               Owner of Collection
        :param continuation:                        Continuation string
        :param size:                                Size of returns
        """

        temp = ''
        param = {}
        self.endpoint = 'https://api-staging.rarible.com/protocol/v0.1/ethereum/nft/collections/byOwner'

        if assertType(self.owner_type, owner):
            if owner is not None:
                param['owner'] = owner

        if assertType(self.continuation_type, continuation):
            if continuation is not None:
                param['continuation'] = continuation

        if assertType(self.size_type, size):
            if size is not None:
                param['size'] = size

        for counter, (key, value) in enumerate(param.items()):
            if counter == 0:
                temp = temp + f'?{key}={value}'
            elif counter > 0:
                temp = temp + f'&{key}={value}'

        self.URLs.append(f'{self.endpoint}{temp}')

    def setQueryAllCollections(self,
                               continuation: Optional[str],
                               size: Optional[int]):
        """
        Gets and sets the parameters needed for querying the entire collection

        :param continuation:                        Continuation String
        :param size:                                Size of returns
        """

        temp = ''
        param = {}
        self.endpoint = 'https://api-staging.rarible.com/protocol/v0.1/ethereum/nft/collections/all'

        if assertType(self.continuation_type, continuation):
            if continuation is not None:
                param['continuation'] = continuation

        if assertType(self.size_type, size):
            if size is not None:
                param['size'] = size

        for counter, (key, value) in enumerate(param.items()):
            if counter == 0:
                temp = temp + f'?{key}={value}'
            elif counter > 0:
                temp = temp + f'&{key}={value}'

        self.URLs.append(f'{self.endpoint}{temp}')

    def parseGenerateNFTID(self):
        pass

    def parseNFTCollectionByID(self):
        pass

    def parseQueryCollectionsByOwner(self):
        pass

    def parseQueryAllCollections(self):
        pass


class OrderOwnership(Rarible):
    def __init__(self):
        super().__init__()

    def setGetNFTOrderByOwnershipID(self,
                                    ownershipId: str):
        """
        Gets and sets the parameters needed for querying NFT orders by ownership ID

        :param ownershipId:                         Ownership ID
        """

        self.endpoint = 'https://api-staging.rarible.com/protocol/v0.1/ethereum/nft-order/ownerships/'

        if assertType(self.ownershipId_type, ownershipId):
            if ownershipId is not None:
                self.endpoint = f'{self.endpoint}{ownershipId}'

        self.URLs.append(self.endpoint)

    def setGetNFTOwnershipByItem(self,
                                 contract: str,
                                 tokenId: int,
                                 continuation: Optional[str],
                                 size: Optional[int]):
        """
        Gets and sets the parameters needed for querying NFT orders by Item

        :param contract:                            Contract Address
        :param tokenId:                             Token ID
        :param continuation:                        Continuation String
        :param size:                                Size of returns
        """

        temp = ''
        param = {}
        self.endpoint = 'https://api-staging.rarible.com/protocol/v0.1/ethereum/nft/collections/all'

        if assertType(self.contract_type, contract):
            if contract is not None:
                param['contract'] = contract

        if assertType(self.tokenId_type, tokenId):
            if tokenId is not None:
                param['tokenId'] = tokenId

        if assertType(self.continuation_type, continuation):
            if continuation is not None:
                param['continuation'] = continuation

        if assertType(self.size_type, size):
            if size is not None:
                param['size'] = size

        for counter, (key, value) in enumerate(param.items()):
            if counter == 0:
                temp = temp + f'?{key}={value}'
            elif counter > 0:
                temp = temp + f'&{key}={value}'

        self.URLs.append(f'{self.endpoint}{temp}')

    def setGetAllNFTOwnership(self,
                              continuation: Optional[str],
                              size: Optional[int]):
        """
        Gets and sets the parameters needed for querying all NFT orders

        :param continuation:                        Continuation String
        :param size:                                Size of returns
        """

        temp = ''
        param = {}
        self.endpoint = 'https://api-staging.rarible.com/protocol/v0.1/ethereum/nft-order/ownerships/all'

        if assertType(self.continuation_type, continuation):
            if continuation is not None:
                param['continuation'] = continuation

        if assertType(self.size_type, size):
            if size is not None:
                param['size'] = size

        for counter, (key, value) in enumerate(param.items()):
            if counter == 0:
                temp = temp + f'?{key}={value}'
            elif counter > 0:
                temp = temp + f'&{key}={value}'

        self.URLs.append(f'{self.endpoint}{temp}')

    def parseGetNFTOrderByOwnershipID(self):
        pass

    def parseGetNFTOwnershipByItem(self):
        pass

    def parseGetAllNFTOwnership(self):
        pass


class OrderItem(Rarible):
    def __init__(self):
        super().__init__()

    def setNFTOrderItemByID(self,
                            itemId: str,
                            includeMeta: Optional[bool]):
        """
        Gets and sets parameters for querying NFT order by Item ID

        :param itemId:                              Item ID
        :param includeMeta:                         Return Metadata for Item
        """

        self.endpoint = 'https://api-staging.rarible.com/protocol/v0.1/ethereum/nft-order/items/'

        if assertType(self.itemId_type, itemId):
            if itemId is not None:
                self.endpoint = f'{self.endpoint}{itemId}/meta'

        if assertType(self.includeMeta_type, includeMeta):
            if includeMeta is not None:
                self.endpoint = f'{self.endpoint}{str(includeMeta).lower()}'

        self.URLs.append(self.endpoint)

    def setNFTOrderItemMetaByID(self,
                                itemId: str):
        """
        Gets and sets parameters for querying NFT order by Item ID

        :param itemId:                              Item ID
        """

        self.endpoint = 'https://api-staging.rarible.com/protocol/v0.1/ethereum/nft-order/items/'

        if assertType(self.itemId_type, itemId):
            if itemId is not None:
                self.URLs.append(f'{self.endpoint}{itemId}/meta')

    def setNFTLazyItemByID(self,
                           itemId: str):
        """
        Gets and sets parameters for lazy querying NFT by Item ID

        :param itemId:                              Item ID
        """

        self.endpoint = 'https://api-staging.rarible.com/protocol/v0.1/ethereum/nft-order/items/'

        if assertType(self.itemId_type, itemId):
            if itemId is not None:
                self.URLs.append(f'{self.endpoint}{itemId}/lazy')

    def setNFTOrderItemByOwner(self,
                               owner: str,
                               continuation: Optional[str],
                               size: Optional[int],
                               includeMeta: Optional[bool]):
        """
        Gets and sets parameters for querying NFT by owner

        :param owner:                               Owner
        :param continuation:                        Continuation String
        :param size:                                Size
        :param includeMeta:                         Include Metadata for NFT in response
        """

        temp = ''
        param = {}

        self.endpoint = 'https://api-staging.rarible.com/protocol/v0.1/ethereum/nft-order/items/byOwner'

        if assertType(self.owner_type, owner):
            if owner is not None:
                param['owner'] = owner

        if assertType(self.itemId_type, continuation):
            if continuation is not None:
                param['continuation'] = continuation

        if assertType(self.size_type, size):
            if size is not None:
                param['size'] = size

        if assertType(self.includeMeta_type, includeMeta):
            if includeMeta is not None:
                param['includeMeta'] = includeMeta

        for counter, (key, value) in enumerate(param.items()):
            if counter == 0:
                temp = temp + f'?{key}={value}'
            elif counter > 0:
                temp = temp + f'&{key}={value}'

        self.URLs.append(f'{self.endpoint}{temp}')

    def setNFTOrderItemByCreator(self,
                                 creator: str,
                                 continuation: Optional[str],
                                 size: Optional[int],
                                 includeMeta: Optional[bool]):
        """
        Gets and sets parameters for querying NFT by creator

        :param creator:                             Creator name
        :param continuation:                        Continuation String
        :param size:                                Size
        :param includeMeta:                         Include Metadata for NFT in response
        """

        temp = ''
        param = {}

        self.endpoint = 'https://api-staging.rarible.com/protocol/v0.1/ethereum/nft-order/items/byCreator'

        if assertType(self.creator_type, creator):
            if creator is not None:
                param['creator'] = creator

        if assertType(self.itemId_type, continuation):
            if continuation is not None:
                param['continuation'] = continuation

        if assertType(self.size_type, size):
            if size is not None:
                param['size'] = size

        if assertType(self.includeMeta_type, includeMeta):
            if includeMeta is not None:
                param['includeMeta'] = includeMeta

        for counter, (key, value) in enumerate(param.items()):
            if counter == 0:
                temp = temp + f'?{key}={value}'
            elif counter > 0:
                temp = temp + f'&{key}={value}'

        self.URLs.append(f'{self.endpoint}{temp}')

    def setNFTItemByCollection(self,
                               collection: str,
                               continuation: Optional[str],
                               size: Optional[int],
                               includeMeta: Optional[bool]):
        """
        Gets and sets parameters for querying NFT by collection

        :param collection:                          Collection
        :param continuation:                        Continuation String
        :param size:                                Size
        :param includeMeta:                         Include Metadata for NFT in response
        """

        temp = ''
        param = {}

        self.endpoint = 'https://api-staging.rarible.com/protocol/v0.1/ethereum/nft-order/items/byCollection'

        if assertType(self.collection_type, collection):
            if collection is not None:
                param['collection'] = collection

        if assertType(self.itemId_type, continuation):
            if continuation is not None:
                param['continuation'] = continuation

        if assertType(self.size_type, size):
            if size is not None:
                param['size'] = size

        if assertType(self.includeMeta_type, includeMeta):
            if includeMeta is not None:
                param['includeMeta'] = includeMeta

        for counter, (key, value) in enumerate(param.items()):
            if counter == 0:
                temp = temp + f'?{key}={value}'
            elif counter > 0:
                temp = temp + f'&{key}={value}'

        self.URLs.append(f'{self.endpoint}{temp}')

    def setNFTAllItems(self,
                       continuation: Optional[str],
                       size: Optional[int],
                       showDeleted: Optional[bool],
                       lastUpdatedFrom: Optional[int],
                       lastUpdatedTo: Optional[int],
                       includeMeta: Optional[bool]):
        """
        Gets and sets parameters for querying all NFT

        :param continuation:                        Continuation String
        :param size:                                Size
        :param showDeleted:                         Show Deleted
        :param lastUpdatedFrom:                     Last Updated Form
        :param lastUpdatedTo:                       Last Updated To
        :param includeMeta:                         Include Metadata for NFT in response
        """

        temp = ''
        param = {}
        self.endpoint = 'https://api-staging.rarible.com/protocol/v0.1/ethereum/nft-order/items/all'

        if assertType(self.continuation_type, continuation):
            if continuation is not None:
                param['continuation'] = continuation

        if assertType(self.size_type, size):
            if size is not None:
                param['size'] = size

        if assertType(self.showDeleted_type, showDeleted):
            if showDeleted is not None:
                param['showDeleted'] = showDeleted

        if assertType(self.lastUpdatedFrom_type, lastUpdatedFrom):
            if lastUpdatedFrom is not None:
                param['lastUpdatedFrom'] = lastUpdatedFrom

        if assertType(self.lastUpdatedTo_type, lastUpdatedTo):
            if lastUpdatedTo is not None:
                param['lastUpdatedTo'] = lastUpdatedTo

        if assertType(self.includeMeta_type, includeMeta):
            if includeMeta is not None:
                param['includeMeta'] = includeMeta

        for counter, (key, value) in enumerate(param.items()):
            if counter == 0:
                temp = temp + f'?{key}={value}'
            elif counter > 0:
                temp = temp + f'&{key}={value}'

        self.URLs.append(f'{self.endpoint}{temp}')

    def parseNFTOrderItemByID(self):
        pass

    def parseNFTOrderItemMetaByID(self):
        pass

    def parseNFTLazyItemByID(self):
        pass

    def parseNFTOrderItemByOwner(self):
        pass

    def parseNFTOrderItemByCreator(self):
        pass

    def parseNFTItemByCollection(self):
        pass

    def parseNFTAllItems(self):
        pass


class OrderActivity(Rarible):
    def __init__(self):
        super().__init__()

    def setNFTOrderActivityByUser(self,
                                  type_: str,
                                  user: str,
                                  continuation: Optional[str],
                                  size: Optional[int]):
        """
        Gets and sets the parameters used for querying order activity by user

        :param type_:                               Type of activity to track and return
        :param user:                                User Address
        :param continuation:                        Continuation String
        :param size:                                Size of returns
        """

        temp = ''
        param = {}
        self.endpoint = 'https://api-staging.rarible.com/protocol/v0.1/ethereum/nft-order/activities/byUser'

        if assertType(self.type_type, type_, conditions=self.type_conditions):
            if type_ is not None:
                param['type'] = type_

        if assertType(self.user_type, user):
            if user is not None:
                param['user'] = user

        if assertType(self.continuation_type, continuation):
            if continuation is not None:
                param['continuation'] = continuation

        if assertType(self.size_type, size):
            if size is not None:
                param['size'] = size

        for counter, (key, value) in enumerate(param.items()):
            if counter == 0:
                temp = temp + f'?{key}={value}'
            elif counter > 0:
                temp = temp + f'&{key}={value}'

        self.URLs.append(f'{self.endpoint}{temp}')

    def setNFTOrderActivityByItem(self,
                                  type_: str,
                                  contract: str,
                                  tokenId: int,
                                  continuation: Optional[str],
                                  size: Optional[int]):
        """
        Gets and sets the parameters used for querying order activity by item

        :param type_:                               Type of activity to track and return
        :param contract:                            Contract Address
        :param tokenId:                             Token ID
        :param continuation:                        Continuation String
        :param size:                                Size of returns
        :return:
        """

        temp = ''
        param = {}
        self.endpoint = 'https://api-staging.rarible.com/protocol/v0.1/ethereum/nft-order/activities/byItem'

        if assertType(self.type_type, type_, conditions=self.type_conditions):
            if type_ is not None:
                param['type'] = type_

        if assertType(self.contract_type, contract):
            if contract is not None:
                param['contract'] = contract

        if assertType(self.tokenId_type, tokenId):
            if tokenId is not None:
                param['tokenId'] = tokenId

        if assertType(self.continuation_type, continuation):
            if continuation is not None:
                param['continuation'] = continuation

        if assertType(self.size_type, size):
            if size is not None:
                param['size'] = size

        for counter, (key, value) in enumerate(param.items()):
            if counter == 0:
                temp = temp + f'?{key}={value}'
            elif counter > 0:
                temp = temp + f'&{key}={value}'

        self.URLs.append(f'{self.endpoint}{temp}')

    def setNFTOrderActivityByCollection(self,
                                        type_: str,
                                        collection: str,
                                        continuation: Optional[str],
                                        size: Optional[int]):
        """
        Gets and Sets the parameters used for querying order activity by collection

        :param type_:                               Type of activity to track and return
        :param collection:                          Collection Address
        :param continuation:                        Continuation String
        :param size:                                Size of returns
        """

        temp = ''
        param = {}
        self.endpoint = 'https://api-staging.rarible.com/protocol/v0.1/ethereum/nft-order/activities/byItem'

        if assertType(self.type_type, type_, conditions=self.type_conditions):
            if type_ is not None:
                param['type'] = type_

        if assertType(self.collection_type, collection):
            if collection is not None:
                param['collection'] = collection

        if assertType(self.continuation_type, continuation):
            if continuation is not None:
                param['continuation'] = continuation

        if assertType(self.size_type, size):
            if size is not None:
                param['size'] = size

        for counter, (key, value) in enumerate(param.items()):
            if counter == 0:
                temp = temp + f'?{key}={value}'
            elif counter > 0:
                temp = temp + f'&{key}={value}'

        self.URLs.append(f'{self.endpoint}{temp}')

    def setAllNFTOrderActivity(self,
                               type_: str,
                               continuation: Optional[str],
                               size: Optional[int]):
        """
        Gets and Sets the parameters used for querying order activity by collection

        :param type_:                               Type of activity to track and return
        :param continuation:                        Continuation String
        :param size:                                Size of returns
        """

        temp = ''
        param = {}
        self.endpoint = 'https://api-staging.rarible.com/protocol/v0.1/ethereum/nft-order/activities/all'

        if assertType(self.type_type, type_, conditions=self.type_conditions):
            if type_ is not None:
                param['type'] = type_

        if assertType(self.continuation_type, continuation):
            if continuation is not None:
                param['continuation'] = continuation

        if assertType(self.size_type, size):
            if size is not None:
                param['size'] = size

        for counter, (key, value) in enumerate(param.items()):
            if counter == 0:
                temp = temp + f'?{key}={value}'
            elif counter > 0:
                temp = temp + f'&{key}={value}'

        self.URLs.append(f'{self.endpoint}{temp}')

    def parseNFTOrderActivityByUser(self):
        pass

    def parseNFTOrderActivityByItem(self):
        pass

    def parseNFTOrderActivityByCollection(self):
        pass

    def parseAllNFTOrderActivity(self):
        pass


class OrderCollection(Rarible):
    def __init__(self):
        super().__init__()

    def setGenerateNFTOrderTokenID(self,
                                   collection: str,
                                   minter: str):
        """
        Gets and sets the parameters needed to query for the next available tokenId for minter

        :param collection:                          Address of Collection
        :param minter:                              Minter Address
        """

        self.endpoint = 'https://api-staging.rarible.com/protocol/v0.1/ethereum/nft-order/collections/'

        if assertType(self.collection_type, collection):
            if collection is not None:
                self.endpoint = f'{self.endpoint}{collection}/generate_token_id'

        if assertType(self.minter_type, minter):
            if minter is not None:
                self.endpoint = f'{self.endpoint}?minter={minter}'

        self.URLs.append(self.endpoint)

    def setNFTOrderCollectionByID(self,
                                  collection: str):
        """
        Gets and sets the parameters needed for querying a collection by ID
        :param collection:                          Address of Collection
        """

        self.endpoint = 'https://api-staging.rarible.com/protocol/v0.1/ethereum/nft-order/collections/'

        if assertType(self.collection_type, collection):
            if collection is not None:
                self.endpoint = f'{self.endpoint}{collection}'

        self.URLs.append(self.endpoint)

    def setQueryNFTOrderCollectionsByOwner(self,
                                           owner: str,
                                           continuation: Optional[str],
                                           size: Optional[int]):
        """
        Gets and sets the parameters needed for querying collections by owner

        :param owner:                               Owner of Collection
        :param continuation:                        Continuation string
        :param size:                                Size of returns
        """

        temp = ''
        param = {}
        self.endpoint = 'https://api-staging.rarible.com/protocol/v0.1/ethereum/nft-order/collections/byOwner'

        if assertType(self.owner_type, owner):
            if owner is not None:
                param['owner'] = owner

        if assertType(self.continuation_type, continuation):
            if continuation is not None:
                param['continuation'] = continuation

        if assertType(self.size_type, size):
            if size is not None:
                param['size'] = size

        for counter, (key, value) in enumerate(param.items()):
            if counter == 0:
                temp = temp + f'?{key}={value}'
            elif counter > 0:
                temp = temp + f'&{key}={value}'

        self.URLs.append(f'{self.endpoint}{temp}')

    def setQueryAllNFTOrderCollections(self,
                                       continuation: Optional[str],
                                       size: Optional[int]):
        """
        Gets and sets the parameters needed for querying the entire collection

        :param continuation:                        Continuation String
        :param size:                                Size of returns
        """

        temp = ''
        param = {}
        self.endpoint = 'https://api-staging.rarible.com/protocol/v0.1/ethereum/nft-order/collections/all'

        if assertType(self.continuation_type, continuation):
            if continuation is not None:
                param['continuation'] = continuation

        if assertType(self.size_type, size):
            if size is not None:
                param['size'] = size

        for counter, (key, value) in enumerate(param.items()):
            if counter == 0:
                temp = temp + f'?{key}={value}'
            elif counter > 0:
                temp = temp + f'&{key}={value}'

        self.URLs.append(f'{self.endpoint}{temp}')

    def parseGenerateNFTOrderTokenID(self):
        pass

    def parseNFTOrderCollectionByID(self):
        pass

    def parseQueryNFTOrderCollectionsByOwner(self):
        pass

    def parseQueryAllNFTOrderCollections(self):
        pass
