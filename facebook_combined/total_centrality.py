import utils as centrality_utils


def main():
    # Create lists
    facebook_path = "facebook_combined/facebook_combined.txt"
    facebook_network = centrality_utils.load_network(facebook_path)
    print("Networks loaded successfully.")
    degree_list = centrality_utils.get_degree_list(facebook_network)
    print("Degrees calculated successfully.")
    betweenness_list = centrality_utils.get_betweenness_centrality_list(facebook_network)
    print("Betweenness calculated successfully.")
    eigenvector_list = centrality_utils.get_eigenvector_centrality_list(facebook_network)
    print("Eigenvectors calculated successfully.")

    # Print statistics
    print(f"Nodes in degree list: {len(degree_list)}")
    print(f"Nodes in betweenness list: {len(betweenness_list)}")
    print(f"Nodes in eigenvector list: {len(eigenvector_list)}")

    # Top-K overlap
    k = 0.1
    top_degree = degree_list[0:int(k * len(degree_list))]
    top_betweenness = betweenness_list[0:int(k * len(betweenness_list))]
    top_eigenvector = eigenvector_list[0:int(k*len(eigenvector_list))]

    print(f"Nodes in degree list: {len(top_degree)}")
    print(f"Nodes in betweenness list: {len(top_betweenness)}")
    print(f"Nodes in eigenvector list: {len(top_eigenvector)}")

    overlap = set(map(lambda x: x[0], top_degree)).intersection(set(map(lambda x: x[0], top_betweenness)))
    print(f"Overlap between top k of degree and betweenness: {len(overlap)}")

    overlap = set(map(lambda x: x[0], top_degree)).intersection(set(map(lambda x: x[0], top_eigenvector)))
    print(f"Overlap between top k of degree and eigenvector: {len(overlap)}")

    overlap = set(map(lambda x: x[0], top_eigenvector)).intersection(set(map(lambda x: x[0], top_betweenness)))
    print(f"Overlap between top k of eigenvector and betweenness: {len(overlap)}")


    ego_list = ["0", "107", "348", "414", "686", "698", "1684", "1912", "3437", "3980"]
    empty_features = ["0"] * 1283
    #my_dict = dict()
    #current_features = empty_features.copy()
    #my_dict["0"] = current_features
    #empty_features[0] = 1
    #print(my_dict["0"][0])

    node_feature_dict = dict()
    feature_idx_type_dict = dict()
    
    #count = 0
    for ego in ego_list:
    #    current_feature_dict = dict()
    #for ego in ["0", "107"]:
        ego_featname = "facebook_combined/facebook/" + ego + ".featnames"
        ego_feat = "facebook_combined/facebook/" + ego + ".egofeat"
        ego_node_feat = "facebook_combined/facebook/" + ego + ".feat"
        ego_to_global_feat = []

        with open(ego_featname, 'r') as file:
            for line in file:
                first_partition = line.split("anonymized feature ")
                second_partition = first_partition[0].split(" ")
                index = int(second_partition[0])
                feature_type = second_partition[1]
                global_feature_index = int(first_partition[1])
                ego_to_global_feat.append(global_feature_index)
                feature_idx_type_dict[str(global_feature_index)] = feature_type

        with open(ego_feat, 'r') as file:
            for line in file:
                #node = int(line.split(" ")[0])
                node = ego
                node_ego_feats = line.split(" ")
                
                current_features = empty_features.copy()
                for i in range(len(node_ego_feats)):
                    node_ego_feat = node_ego_feats[i]
                    if (node_ego_feat == "1"):
                        current_features[ego_to_global_feat[i]] = "1"
                node_feature_dict[str(node)] = current_features
        
        with open(ego_node_feat, 'r') as file:
            for line in file:
                node = int(line.split(" ")[0])
                #print(node)
                node_ego_feats = line.split(" ")[1:]
                
                current_features = empty_features.copy()
                for i in range(len(node_ego_feats)):
                    node_ego_feat = node_ego_feats[i]
                    if (node_ego_feat == "1"):
                        current_features[ego_to_global_feat[i]] = "1"
                if (not(str(node) in node_feature_dict.keys() or str(node) in ego_list)):
                    node_feature_dict[str(node)] = current_features

    node_feature_file = "facebook_combined/node_to_features.txt"    
    with open(node_feature_file, 'w') as file:
        for key in node_feature_dict.keys():
            file.write(key)
            file.write(";")
            features = node_feature_dict[key]
            file.write(",".join(features))
            file.write("\n")

    feature_type_file = "facebook_combined/feature_to_type.txt"    
    with open(feature_type_file, 'w') as file:
        for key in feature_idx_type_dict.keys():
            file.write(key)
            file.write(":")
            types = feature_idx_type_dict[key]
            file.write(types)
            file.write("\n")

    

                

    #print(node_feature_dict["0"])
    #print(len(node_feature_dict.keys()))
    #for i in range(len(node_feature_dict.keys())):
    #    if str(i) not in node_feature_dict.keys():
    #        print(i)

main()