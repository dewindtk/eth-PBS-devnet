package main

import (
	"testing"

	boostTypes "github.com/flashbots/go-boost-utils/types"
	"github.com/flashbots/mev-boost-relay/common"
	"github.com/stretchr/testify/require"
)

// TestValidatorRegistrationSignature can be used to validate the signature of an arbitrary validator registration
func TestValidatorRegistrationSignature(t *testing.T) {
	// Fill in validator registration details
	pubkey := "0x84e975405f8691ad7118527ee9ee4ed2e4e8bae973f6e29aa9ca9ee4aea83605ae3536d22acc9aa1af0545064eacf82e"
	gasLimit := 30000000
	feeRecipient := "0xdb65fed33dc262fe09d9a2ba8f80b329ba25f941"
	timestamp := 1606824043
	signature := "0xaf12df007a0c78abb5575067e5f8b089cfcc6227e4a91db7dd8cf517fe86fb944ead859f0781277d9b78c672e4a18c5d06368b603374673cf2007966cece9540f3a1b3f6f9e1bf421d779c4e8010368e6aac134649c7a009210780d401a778a5"

	// Constructing the object
	payload := boostTypes.SignedValidatorRegistration{
		Message: &boostTypes.RegisterValidatorRequestMessage{
			GasLimit:  uint64(gasLimit),
			Timestamp: uint64(timestamp),
		},
	}

	var err error
	payload.Message.Pubkey, err = boostTypes.HexToPubkey(pubkey)
	require.NoError(t, err)
	payload.Signature, err = boostTypes.HexToSignature(signature)
	require.NoError(t, err)
	payload.Message.FeeRecipient, err = boostTypes.HexToAddress(feeRecipient)
	require.NoError(t, err)

	mainnetDetails, err := common.NewEthNetworkDetails(common.EthNetworkMainnet)
	require.NoError(t, err)

	ok, err := boostTypes.VerifySignature(payload.Message, mainnetDetails.DomainBuilder, payload.Message.Pubkey[:], payload.Signature[:])
	require.NoError(t, err)
	require.True(t, ok)
}
