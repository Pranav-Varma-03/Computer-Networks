import sys
from block import State

import time
import peers_manager
import pieces_manager
import torrent
import tracker
import logging
import os
import message
from rarest_piece import RarestPieces

class Run(object):
    percentage_completed = -1
    last_log_line = ""

    def __init__(self):
        try:
            torrent_file = sys.argv[1]
        except IndexError:
            logging.error("No torrent file provided!")
            sys.exit(0)
        self.torrent = torrent.Torrent().load_from_path(torrent_file)
        self.tracker = tracker.Tracker(self.torrent)

        self.pieces_manager = pieces_manager.PiecesManager(self.torrent)
        self.peers_manager = peers_manager.PeersManager(self.torrent, self.pieces_manager)

        self.peers_manager.start()
        logging.info("PeersManager Started")
        logging.info("PiecesManager Started")
    
    def nget_sorted_pieces(self,peers,pieces):
        list = [ ] 
        for piece in pieces:
            dic = { "piece" : piece , "value" : 0 }
            for peer in peers:
                if(peer.has_piece(piece.piece_index)):
                    dic["value"] += 1     
            list.append(dic) 
        
        sorted_data = sorted(list, key=lambda x: x["value"])
        sorted_piece_list = []
        for  d in sorted_data:
            sorted_piece_list.append(d["piece"])

        # for rare in sorted_data:
        #     logging.info(f'Piece Ind: {rare["piece"].piece_index}, #Peers = {rare["value"]}')

        return sorted_piece_list,sorted_data       

    def start(self):
        peers_dict = self.tracker.get_peers_from_trackers()
        self.peers_manager.add_peers(peers_dict.values())
        
        while not self.pieces_manager.all_pieces_completed():
            if not self.peers_manager.has_unchoked_peers():
                time.sleep(1)
                logging.info("No unchocked peers")
                continue
            
            # index = self.peers_manager.rarest_piece1(counter)
            list1,sorted_data = self.nget_sorted_pieces(self.peers_manager.peers,self.pieces_manager.pieces)
            for rare in sorted_data:
                logging.info(f'Piece Ind: {rare["piece"].piece_index}, #Peers = {rare["value"]}')

            for piece in list1:
                index = piece.piece_index
            
                # index = self.peers_manager.rarest_piece1(counter)
            
                
                if index is None or self.pieces_manager.pieces[index].is_full:
                 continue

                peer = self.peers_manager.get_random_peer_having_piece(index)
                if not peer:
                 continue

                self.pieces_manager.pieces[index].update_block_status()

                data = self.pieces_manager.pieces[index].get_empty_block()
                if not data:
                 continue

                piece_index, block_offset, block_length = data
                piece_data = message.Request(piece_index, block_offset, block_length).to_bytes()
                peer.send_to_peer(piece_data)

                self.display_progression()

            time.sleep(0.1)

        logging.info("File(s) downloaded successfully.")
        self.display_progression()

        self._exit_threads()

    def display_progression(self):
        new_progression = 0

        for i in range(self.pieces_manager.number_of_pieces):
            for j in range(self.pieces_manager.pieces[i].number_of_blocks):
                if self.pieces_manager.pieces[i].blocks[j].state == State.FULL:
                    new_progression += len(self.pieces_manager.pieces[i].blocks[j].data)

        if new_progression == self.percentage_completed:
            return

        number_of_peers = self.peers_manager.unchoked_peers_count()
        percentage_completed = float((float(new_progression) / self.torrent.total_length) * 100)

        current_log_line = "Connected peers: {} - {}% completed | {}/{} pieces".format(number_of_peers,
                                                                                         round(percentage_completed, 2),
                                                                                         self.pieces_manager.complete_pieces,
                                                                                         self.pieces_manager.number_of_pieces)
        if current_log_line != self.last_log_line:
            print(current_log_line)

        self.last_log_line = current_log_line
        self.percentage_completed = new_progression

    def _exit_threads(self):
        self.peers_manager.is_active = False
        os._exit(0)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    run = Run()
    run.start()