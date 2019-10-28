src/kudu/rpc/acceptor_pool.cc
rpc_connections_accepted comment:Number of incoming TCP connections made to the RPC server

src/kudu/rpc/service_pool.cc
rpc_incoming_queue_time comment:Number of microseconds incoming RPC requests spend in the worker queue
rpcs_queue_overflow comment:Number of RPCs dropped because the service queue was full.
rpcs_timed_out_in_queue comment:Number of RPCs whose timeout elapsed while waiting in the service queue, and thus were not processed.

src/kudu/tserver/scanners.cc
active_scanners comment:Number of scanners that are currently active 

src/kudu/util/block_cache_metrics.cc
block_cache_evictions comment:Number of blocks evicted from the cache
block_cache_hits comment:Number of lookups that found a block
block_cache_hits_caching comment:Number of lookups that were expecting a block that found one.Use this number instead of cache_hits when trying to determine how efficient the cache is
block_cache_inserts comment:Number of blocks inserted in the cache
block_cache_lookups comment:Number of blocks looked up from the cache
block_cache_misses comment:Number of lookups that didn't yield a block
block_cache_misses_caching comment:Number of lookups that were expecting a block that didn't yield one.Use this number instead of cache_misses when trying to determine how efficient the cache is
block_cache_usage comment:Memory consumed by the block cache

src/kudu/fs/block_manager_metrics.cc
block_manager_blocks_open_reading comment:Number of data blocks currently open for reading
block_manager_blocks_open_writing comment:Number of data blocks currently open for writing
block_manager_total_blocks_created comment:Number of data blocks that were created since service start
block_manager_total_blocks_deleted comment:Number of data blocks that were deleted since service start
block_manager_total_bytes_read comment:Number of bytes of block data read since service start
block_manager_total_bytes_written comment:Number of bytes of block data written since service start
block_manager_total_disk_sync comment:Number of disk synchronizations of block data since service start
block_manager_total_readable_blocks comment:Number of data blocks opened for reading since service start
block_manager_total_writable_blocks comment:Number of data blocks opened for writing since service start


codegen/compilation_manager.cc
code_cache_hits comment:Number of codegen cache hits since start
code_cache_queries comment:Number of codegen cache queries (hits + misses)since start

util/thread.cc
cpu_stime comment:Total system CPU time of the process
cpu_utime comment:Total user CPU time of the process

fs/data_dirs.cc
data_dirs_failed comment:Number of data directories whose disks are currently in a failed state
data_dirs_full comment:Number of data directories whose disks are currently full

util/file_cache_metrics.cc
file_cache_evictions comment:Number of file descriptors evicted from the cache
file_cache_hits comment:Number of lookups that found a file descriptor
file_cache_hits_caching comment:Number of lookups that were expecting a file descriptor that found one. Use this number instead of cache_hits when trying to determine how efficient the cache is
file_cache_inserts comment:Number of file descriptors inserted in the cache
file_cache_lookups comment:Number of file descriptors looked up from the cache
file_cache_misses comment:Number of lookups that didn't yield a file descriptor
file_cache_misses_caching comment:Number of lookups that were expecting a file descriptor that didn't yield one. Use this number instead of cache_misses when trying to determine how efficient the cache is
file_cache_usage comment:Number of entries in the file cache

server/tcmalloc_metrics.cc
generic_current_allocated_bytes comment:Number of bytes used by the application. This will not typically match the memory use reported by the OS, because it does not include TCMalloc overhead or memory fragmentation. (Disabled - no tcmalloc in this build)
generic_heap_size comment:Bytes of system memory reserved by TCMalloc. (Disabled - no tcmalloc in this build)

./server/glog_metrics.cc
glog_error_messages comment:Number of ERROR-level log messages emitted by the application.
glog_info_messages comment:Number of INFO-level log messages emitted by the application.
glog_warning_messages comment:Number of WARNING-level log messages emitted by the application.

src/kudu/clock/hybrid_clock.cc
hybrid_clock_error comment:Server clock maximum error.
hybrid_clock_timestamp comment:Hybrid clock timestamp.

./src/kudu/util/thread.cc
involuntary_context_switches comment:Total involuntary context switches 

./src/kudu/fs/log_block_manager.cc
log_block_manager_blocks_under_management comment:Number of data blocks currently under management
log_block_manager_bytes_under_management comment:Number of bytes of data blocks currently under management
log_block_manager_containers comment:Number of log block containers
log_block_manager_dead_containers_deleted comment:Number of full (but dead) block containers that were deleted
log_block_manager_full_containers comment:Number of full log block containers
log_block_manager_holes_punched comment:Number of holes punched since service start

./src/kudu/kserver/kserver.cc
op_apply_queue_length comment:Number of operations waiting to be applied to the tablet. High queue lengths indicate that the server is unable to process operations as fast as they are being written to the WAL.
op_apply_queue_time comment:Time that operations spent waiting in the apply queue before being processed. High queue times indicate that the server is unable to process operations as fast as they are being written to the WAL.
op_apply_run_time comment:Time that operations spent being applied to the tablet. High values may indicate that the server is under-provisioned or that operations consist of very large batches.

./src/kudu/rpc/reactor.cc
reactor_active_latency_us comment:Histogram of the wall clock time for reactor thread wake-ups. The reactor thread is responsible for all network I/O and therefore outliers in this latency histogram directly contribute to the latency of both inbound and outbound RPCs.
reactor_load_percent comment:The percentage of time that the reactor is busy (not blocked awaiting network activity). If this metric shows significant samples nears 100%, increasing the number of reactors may be beneficial.

./src/kudu/tserver/scanner_metrics.cc
scanner_duration comment:Scanner Duration(Histogram of the duration of active scanners on this server)
scanners_expired comment:Scanners Expired(Number of scanners that have expired due to inactivity since service start)

./src/kudu/util/spinlock_profiling.cc
spinlock_contention_time comment:Amount of time consumed by contention on internal spinlocks since the server started. If this increases rapidly, it may indicate a performance issue in Kudu internals triggered by a particular workload and warrant investigation.

./src/kudu/tserver/tablet_copy_client.cc
tablet_copy_bytes_fetched comment:Number of bytes fetched during tablet copy operations since server start
tablet_copy_open_client_sessions comment:Number of currently open tablet copy client sessions on this server

./src/kudu/tserver/tablet_copy_source_session.cc
tablet_copy_bytes_sent comment:Number of bytes sent during tablet copy operations since server start
tablet_copy_open_source_sessions comment:Number of currently open tablet copy source sessions on this server

src/kudu/tserver/ts_tablet_manager.cc
tablets_num_bootstrapping comment:Number of tablets currently bootstrapping
tablets_num_failed comment:Number of failed tablets
tablets_num_initialized comment:Number of tablets currently initialized
tablets_num_not_initialized comment:Number of tablets currently not initialized
tablets_num_running comment:Number of tablets currently running
tablets_num_shutdown comment:Number of tablets currently shut down
tablets_num_stopped comment:Number of tablets currently stopped
tablets_num_stopping comment:Number of tablets currently stopping

./src/kudu/server/tcmalloc_metrics.cc
tcmalloc_current_total_thread_cache_bytes comment:Thread Cache Memory Usage(A measure of some of the memory TCMalloc is using (for small objects).)TCM_ASAN_MSG)
tcmalloc_max_total_thread_cache_bytes comment:Thread Cache Memory Limit(A limit to how much memory TCMalloc dedicates for small objects. Higher numbers trade off more memory use for -- in some situations -- improved efficiency.)
tcmalloc_pageheap_free_bytes comment:Free Heap Memory("Number of bytes in free, mapped pages in page heap. These bytes can be used to fulfill allocation requests. They always count towards virtual memory usage, and unless the underlying memory is swapped out by the OS, they also count towards physical memory usage.)
tcmalloc_pageheap_unmapped_bytes comment:Unmapped Heap Memory(Number of bytes in free, unmapped pages in page heap. These are bytes that have been released back to the OS, possibly by one of the MallocExtension \"Release\" calls. They can be used to fulfill allocation requests, but typically incur a page fault. They always count towards virtual memory usage, and depending on the OS, typically do not count towards physical memory usage.)

./src/kudu/util/thread.cc
threads_running comment:Current number of running threads
threads_started comment:Total number of threads started on this server
voluntary_context_switches comment:Total voluntary context switches


handler_latency_kudu_consensus_ConsensusService_BulkChangeConfig
handler_latency_kudu_consensus_ConsensusService_ChangeConfig
handler_latency_kudu_consensus_ConsensusService_GetConsensusState
handler_latency_kudu_consensus_ConsensusService_GetLastOpId
handler_latency_kudu_consensus_ConsensusService_GetNodeInstance
handler_latency_kudu_consensus_ConsensusService_LeaderStepDown
handler_latency_kudu_consensus_ConsensusService_RequestConsensusVote
handler_latency_kudu_consensus_ConsensusService_RunLeaderElection
handler_latency_kudu_consensus_ConsensusService_StartTabletCopy
handler_latency_kudu_consensus_ConsensusService_UnsafeChangeConfig
handler_latency_kudu_consensus_ConsensusService_UpdateConsensus
handler_latency_kudu_server_GenericService_CheckLeaks
handler_latency_kudu_server_GenericService_DumpMemTrackers
handler_latency_kudu_server_GenericService_FlushCoverage
handler_latency_kudu_server_GenericService_GetFlags
handler_latency_kudu_server_GenericService_GetStatus
handler_latency_kudu_server_GenericService_ServerClock
handler_latency_kudu_server_GenericService_SetFlag
handler_latency_kudu_server_GenericService_SetServerWallClockForTests
handler_latency_kudu_tserver_TabletCopyService_BeginTabletCopySession
handler_latency_kudu_tserver_TabletCopyService_CheckSessionActive
handler_latency_kudu_tserver_TabletCopyService_EndTabletCopySession
handler_latency_kudu_tserver_TabletCopyService_FetchData
handler_latency_kudu_tserver_TabletServerAdminService_AlterSchema
handler_latency_kudu_tserver_TabletServerAdminService_CreateTablet
handler_latency_kudu_tserver_TabletServerAdminService_DeleteTablet
handler_latency_kudu_tserver_TabletServerService_Checksum
handler_latency_kudu_tserver_TabletServerService_ListTablets
handler_latency_kudu_tserver_TabletServerService_Ping
handler_latency_kudu_tserver_TabletServerService_Scan
handler_latency_kudu_tserver_TabletServerService_ScannerKeepAlive
handler_latency_kudu_tserver_TabletServerService_SplitKeyRange
handler_latency_kudu_tserver_TabletServerService_Write

