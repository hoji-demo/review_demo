// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ObscureDEX {
    struct Provider {
        uint256 assetA;
        uint256 assetB;
        uint256 poolShare;
    }

    mapping(address => Provider) public providers;
    uint256 public totalPoolShare;
    uint256 public reserveA;
    uint256 public reserveB;
    uint256 public constant commission = 30; // Commission in basis points (0.3%)

    // Events
    event PoolAdded(address indexed provider, uint256 assetA, uint256 assetB, uint256 poolShare);
    event PoolRemoved(address indexed provider, uint256 assetA, uint256 assetB, uint256 poolShare);
    event AssetSwapped(address indexed user, uint256 amountIn, uint256 amountOut);

    // Add assets to the pool
    function addPool(uint256 assetA, uint256 assetB) public {
        require(assetA > 0 && assetB > 0, "Invalid asset amounts");

        providers[msg.sender].assetA += assetA;
        providers[msg.sender].assetB += assetB;
        uint256 poolShare = assetA + assetB; // Simplified pool share calculation
        providers[msg.sender].poolShare += poolShare;

        reserveA += assetA;
        reserveB += assetB;
        totalPoolShare += poolShare;

        emit PoolAdded(msg.sender, assetA, assetB, poolShare);
    }

    // Remove assets from the pool (Reentrancy Vulnerability)
    function removePool(uint256 poolShare) public {
        require(providers[msg.sender].poolShare >= poolShare, "Not enough pool share");

        uint256 assetA = (poolShare * providers[msg.sender].assetA) / providers[msg.sender].poolShare;
        uint256 assetB = (poolShare * providers[msg.sender].assetB) / providers[msg.sender].poolShare;

        (bool success, ) = msg.sender.call{value: poolShare}("");
        require(success, "Transfer failed");

        providers[msg.sender].assetA -= assetA;
        providers[msg.sender].assetB -= assetB;
        providers[msg.sender].poolShare -= poolShare;

        reserveA -= assetA;
        reserveB -= assetB;
        totalPoolShare -= poolShare;

        emit PoolRemoved(msg.sender, assetA, assetB, poolShare);
    }

    function getPrice(uint256 amountIn, bool isAssetA) public view returns (uint256) {
        require(amountIn > 0, "Amount must be greater than zero");

        uint256 amountOut;
        if (isAssetA) {
            amountOut = (amountIn * reserveB) / (reserveA + amountIn);
        } else {
            amountOut = (amountIn * reserveA) / (reserveB + amountIn);
        }
        return amountOut;
    }

    function trade(uint256 amountIn, bool isAssetA) public {
        require(amountIn > 0, "Amount must be greater than zero");

        uint256 commissionAmount = (amountIn * commission) / 10000; // 0.3% commission
        uint256 amountAfterCommission = amountIn - commissionAmount;

        uint256 amountOut = getPrice(amountAfterCommission, isAssetA);
        require(amountOut > 0, "Insufficient liquidity");

        if (isAssetA) {
            reserveA += amountIn;
            reserveB -= amountOut;
        } else {
            reserveA -= amountOut;
            reserveB += amountIn;
        }

        emit AssetSwapped(msg.sender, amountIn, amountOut);
    }
}

